from asyncio.log import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobTitle, JobTitleAssessment
from job_seekers.models import JobProfile, JobProfileAssessment, JobProfileSkill
from .serializers import (
    GetAssessmentQuestionsSerializer,
    JobTitleAssessmentSerializer,
    AssessmentResultRequestSerializer,
    AssessmentResultResponseSerializer,
    GetResultsResponseSerializer,
)
from django.utils import timezone
import logging
from job_seekers.modules.settings.profile_assessment import (
    is_profile_eligible_for_assessment,
)
from .generate_assessment import generate_assessment_questions
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from .models import JobProfileAssessment


class GetAssessmentQuestionsView(APIView):
    @swagger_auto_schema(
        request_body=GetAssessmentQuestionsSerializer,
        responses={
            200: openapi.Response(
                description="Assessment questions retrieved successfully",
                examples={
                    "application/json": {
                        "message": "success",
                        "data": {
                            "assessment_time": "20 minutes",
                            "questions": [
                                {
                                    "question": "What is the primary language used for backend development?",
                                    "options": ["Java", "Python", "C#"],
                                },
                                {
                                    "question": "Which database is commonly used in backend development?",
                                    "options": ["MySQL", "MongoDB", "SQLite"],
                                },
                            ],
                        },
                    }
                },
            ),
            400: "Bad Request",
        },
        operation_description="Get assessment questions based on job title ID.",
    )
    def post(self, request):
        serializer = GetAssessmentQuestionsSerializer(data=request.data)
        if serializer.is_valid():
            job_title_id = serializer.validated_data["job_title_id"]
            job_seeker_id = request.user.id

            try:
                job_title = JobTitle.objects.get(id=job_title_id)
                print(job_title)

                # Check if the profile is eligible for assessment
                is_eligible, job_profile = is_profile_eligible_for_assessment(
                    job_seeker_id
                )

                if not is_eligible:
                    return Response(
                        {"message": "Assessment not allowed"},
                        status=status.HTTP_403_FORBIDDEN,
                    )

                # Extract skills from the JobProfileSkill model
                job_profile_skills = JobProfileSkill.objects.filter(
                    job_profile=job_profile
                )
                skills = [
                    job_profile_skill.skill.name
                    for job_profile_skill in job_profile_skills
                ]
                print(skills)

                # Generate questions using Gemini API
                questions = generate_assessment_questions(job_title.name, skills)

                # Check if the number of generated questions is exactly 30
                if len(questions) != 30:
                    return Response(
                        {
                            "warning": f"The number of questions generated is {len(questions)}, which is not equal to 30."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Save generated questions in the JobTitleAssessment model
                for question in questions:
                    JobTitleAssessment.objects.create(
                        job_title=job_title,
                        question=question["question"],
                        options=question["options"],
                        answer=question["correct_answer"],
                    )

                # Retrieve the questions from the database
                questions = JobTitleAssessment.objects.filter(job_title=job_title)
                question_data = JobTitleAssessmentSerializer(questions, many=True).data

                return Response(
                    {
                        "message": "success",
                        "data": {
                            "assessment_time": "20 minutes",
                            "questions": question_data,
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            except JobTitle.DoesNotExist:
                return Response(
                    {"message": "Job title not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssessmentResultView(APIView):
    @swagger_auto_schema(
        request_body=AssessmentResultRequestSerializer,
        responses={200: AssessmentResultRequestSerializer, 400: "Bad Request"},
        operation_description="Get assessment results.",
        examples={
            "application/json": {
                "job_profile_id": 1,
                "job_title_id": 1,
                "submission": [
                    {"question_id": 1, "selected_option": "A"},
                    {"question_id": 2, "selected_option": "B"},
                    # more submissions
                ],
            }
        },
    )
    def post(self, request):
        serializer = AssessmentResultRequestSerializer(data=request.data)
        if serializer.is_valid():
            job_profile_id = serializer.validated_data["job_profile_id"]
            job_title_id = serializer.validated_data["job_title_id"]
            submission = serializer.validated_data["submission"]

            try:
                job_profile = JobProfile.objects.get(id=job_profile_id)
                job_title = JobTitle.objects.get(id=job_title_id)
            except JobProfile.DoesNotExist:
                return Response(
                    {"error": "JobProfile not found"}, status=status.HTTP_404_NOT_FOUND
                )
            except JobTitle.DoesNotExist:
                return Response(
                    {"error": "JobTitle not found"}, status=status.HTTP_404_NOT_FOUND
                )

            assessments = JobTitleAssessment.objects.filter(job_title=job_title)
            total_marks = assessments.count()
            obtained_marks = 0

            for answer in submission:
                question_id = answer.get("question_id")
                if question_id is None:
                    continue

                try:
                    question = assessments.get(id=question_id)
                    if question.answer == answer["selected_option"]:
                        obtained_marks += 1
                except JobTitleAssessment.DoesNotExist:
                    logger.error(
                        f"JobTitleAssessment with ID {question_id} does not exist."
                    )
                    continue

            status_result = "Pass" if obtained_marks >= 18 else "Fail"

            job_profile_assessment = JobProfileAssessment.objects.create(
                job_profile=job_profile,
                data=request.data,
                obtained_marks=obtained_marks,
                total_marks=total_marks,
                status=status_result,
            )

            response_data = {
                "employee_job_profile_id": job_profile.id,
                "obtained_marks": obtained_marks,
                "total_marks": total_marks,
                "status": status_result,
                "created_at": job_profile_assessment.created_at,
                "updated_at": job_profile_assessment.updated_at,
                "message": "Result Saved",
            }

            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetResultsView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "job_profile_id",
                openapi.IN_QUERY,
                description="Job Profile ID",
                type=openapi.TYPE_INTEGER,
            )
        ],
        responses={200: GetResultsResponseSerializer, 400: "Bad Request"},
        operation_description="Get assessment results based on job profile ID.",
        examples={
            "application/json": {
                "job_profile_id": 1796,
                "test_result": [
                    {"question_id": 1396, "answer": "Critical thinking skills"},
                    {
                        "question_id": 1395,
                        "answer": "Flexibleaccommodating and willing to pitch in to help their colleagues",
                    },
                    # more results
                ],
                "obtained_marks": 22,
                "total_marks": 26,
                "status": "Pass",
                "created_at": "2024-07-10T04:59:51.000000Z",
                "updated_at": "2024-07-10T04:59:51.000000Z",
                "message": "Result Retrieved",
            }
        },
    )
    def get(self, request):
        job_profile_id = request.query_params.get("job_profile_id")
        if not job_profile_id:
            return Response(
                {"message": "Job profile ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            job_profile_assessments = JobProfileAssessment.objects.filter(
                job_profile_id=job_profile_id
            )
            if not job_profile_assessments.exists():
                return Response(
                    {"message": "Job profile assessment not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            response_data_list = []
            for job_profile_assessment in job_profile_assessments:
                try:
                    # Ensure data is in JSON string format
                    if isinstance(job_profile_assessment.data, str):
                        data = json.loads(job_profile_assessment.data)
                    else:
                        data = job_profile_assessment.data

                    test_result = data.get("submission", [])
                except json.JSONDecodeError:
                    return Response(
                        {"message": "Invalid data format in job profile assessment"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

                response_data = {
                    "job_profile_id": job_profile_id,
                    "test_result": test_result,
                    "obtained_marks": job_profile_assessment.obtained_marks,
                    "total_marks": job_profile_assessment.total_marks,
                    "status": job_profile_assessment.status,
                    "created_at": job_profile_assessment.created_at,
                    "updated_at": job_profile_assessment.updated_at,
                    "message": "Result Retrieved",
                }
                response_data_list.append(response_data)

            return Response(response_data_list, status=status.HTTP_200_OK)

        except JobProfileAssessment.DoesNotExist:
            return Response(
                {"message": "Job profile assessment not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
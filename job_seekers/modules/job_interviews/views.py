from asyncio.log import logger
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from .models import ScreeningInterviewTemplate, JobProfileInterview
from job_seekers.models import JobProfileAssessment, JobProfile
from drf_yasg.utils import swagger_auto_schema
from .serializers import (
    ScreeningInterviewTemplateSerializer,
    JobProfileInterviewSerializer,
)


class ScreeningInterviewTemplateQuestionsView(generics.RetrieveAPIView):
    serializer_class = ScreeningInterviewTemplateSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Return an empty queryset for schema generation context
        if getattr(self, "swagger_fake_view", False):
            return ScreeningInterviewTemplate.objects.none()
        return ScreeningInterviewTemplate.objects.all()


class RetrieveInterviewQuestionsView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all interview questions",
        responses={
            200: openapi.Response(
                description="Interview questions retrieved successfully",
                examples={
                    "application/json": {
                        "status": "success",
                        "data": [
                            {
                                "id": 1,
                                "name": "Technical Interview",
                                "status": "active",
                                "questions": "What is polymorphism?",
                                "added_by": "admin",
                            },
                            # more examples
                        ],
                    }
                },
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "User is not authorized to view interview questions.",
                    }
                },
            ),
            500: openapi.Response(
                description="Internal server error",
                examples={
                    "application/json": {
                        "status": "error",
                        "message": "An error occurred while retrieving interview questions.",
                    }
                },
            ),
        },
    )
    def get(self, request):
        job_profile_id = request.query_params.get("job_profile_id")
        logger.debug(f"job_profile_id: {job_profile_id}")

        if not job_profile_id:
            return Response(
                {"status": "error", "message": "Job profile ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            job_profile = JobProfile.objects.get(id=job_profile_id)
            logger.debug(f"JobProfile: {job_profile}")
            assessment = JobProfileAssessment.objects.get(job_profile=job_profile)
            logger.debug(f"JobProfileAssessment: {assessment}")

            if assessment.status.lower() != "pass":
                logger.debug(f"Assessment status: {assessment.status}")
                return Response(
                    {
                        "status": "error",
                        "message": "User is not authorized to view interview questions.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            interview_templates = ScreeningInterviewTemplate.objects.all()
            serializer = ScreeningInterviewTemplateSerializer(
                interview_templates, many=True
            )
            logger.debug(f"Interview Templates: {serializer.data}")
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except JobProfile.DoesNotExist:
            logger.error(f"Job profile not found for ID: {job_profile_id}")
            return Response(
                {"status": "error", "message": "Job profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except JobProfileAssessment.DoesNotExist:
            logger.error(
                f"Job profile assessment not found for profile ID: {job_profile_id}"
            )
            return Response(
                {"status": "error", "message": "Job profile assessment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response(
                {
                    "status": "error",
                    "message": "An error occurred while retrieving interview questions.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class JobProfileInterviewSubmitView(generics.CreateAPIView):
    queryset = JobProfileInterview.objects.all()
    serializer_class = JobProfileInterviewSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "Answers submitted successfully"},
            status=status.HTTP_201_CREATED,
        )

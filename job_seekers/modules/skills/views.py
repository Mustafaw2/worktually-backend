from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from job_seekers.modules.skills.models import Skills
from .serializers import SkillSerializer
from job_seekers.modules.skills.models import Skills, JobProfileSkill
from job_seekers.models import JobProfile
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from lookups.models import SkillCategory
from job_seekers.modules.skills.models import Skills
from job_seekers.modules.skills.serializers import (
    SkillSerializer,
    SkillCategorySerializer,
    AddSkillsToJobProfileSerializer,
    JobProfileSkillSerializer,
)


class AddSkillCategoryView(generics.CreateAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=SkillCategorySerializer,
        responses={
            201: openapi.Response(
                "Skill category added successfully.", SkillCategorySerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a new skill category.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            skill_category = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": SkillCategorySerializer(skill_category).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateSkillCategoryView(generics.UpdateAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=SkillCategorySerializer,
        responses={
            200: openapi.Response(
                "Skill category updated successfully.", SkillCategorySerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing skill category.",
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            skill_category = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": SkillCategorySerializer(skill_category).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteSkillCategoryView(generics.DestroyAPIView):
    queryset = SkillCategory.objects.all()
    serializer_class = SkillCategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Skill category deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a skill category.",
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Skill category deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddSkillsToJobProfileView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddSkillsToJobProfileSerializer

    @swagger_auto_schema(
        request_body=AddSkillsToJobProfileSerializer,
        responses={
            201: openapi.Response("Skills added successfully."),
            400: "Bad Request",
        },
        operation_description="Add multiple skills to a job profile.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            job_profile_id = serializer.validated_data["job_profile_id"]
            skill_ids = serializer.validated_data["skill_ids"]

            # Check if job profile exists
            try:
                job_profile = JobProfile.objects.get(id=job_profile_id)
            except JobProfile.DoesNotExist:
                return Response(
                    {"status": "error", "errors": "Job profile not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Add skills to the job profile
            job_profile_skills = []
            for skill_id in skill_ids:
                try:
                    skill = Skills.objects.get(id=skill_id)
                    job_profile_skill = JobProfileSkill.objects.create(
                        job_profile=job_profile, skill=skill
                    )
                    job_profile_skills.append(job_profile_skill)
                except Skills.DoesNotExist:
                    return Response(
                        {
                            "status": "error",
                            "errors": f"Skill with id {skill_id} not found.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {
                    "status": "success",
                    "data": JobProfileSkillSerializer(
                        job_profile_skills, many=True
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateSkillView(generics.UpdateAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=SkillSerializer,
        responses={
            200: openapi.Response("Skill updated successfully.", SkillSerializer),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing skill.",
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            skill = serializer.save()
            return Response(
                {"status": "success", "data": SkillSerializer(skill).data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteSkillView(generics.DestroyAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Skill deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a skill.",
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Skill deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddJobProfileSkillView(generics.CreateAPIView):
    queryset = JobProfileSkill.objects.all()
    serializer_class = AddSkillsToJobProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=AddSkillsToJobProfileSerializer,
        responses={
            201: openapi.Response(
                "Job Profile Skill added successfully.", AddSkillsToJobProfileSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a skill to a job profile.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            job_profile_id = serializer.validated_data["job_profile_id"]
            skill_ids = serializer.validated_data["skill_ids"]

            # Check if job profile exists
            try:
                job_profile = JobProfile.objects.get(id=job_profile_id)
            except JobProfile.DoesNotExist:
                return Response(
                    {"status": "error", "errors": "Job profile not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Add skills to the job profile
            job_profile_skills = []
            for skill_id in skill_ids:
                try:
                    skill = Skills.objects.get(id=skill_id)
                    job_profile_skill = JobProfileSkill.objects.create(
                        job_profile=job_profile, skill=skill
                    )
                    job_profile_skills.append(job_profile_skill)
                except Skills.DoesNotExist:
                    return Response(
                        {
                            "status": "error",
                            "errors": f"Skill with id {skill_id} not found.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {
                    "status": "success",
                    "data": JobProfileSkillSerializer(
                        job_profile_skills, many=True
                    ).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateJobProfileSkillView(generics.UpdateAPIView):
    queryset = JobProfileSkill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=SkillSerializer,
        responses={
            200: openapi.Response(
                "Job Profile Skill updated successfully.", SkillSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing job profile skill.",
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            job_profile_skill = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": SkillSerializer(job_profile_skill).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteJobProfileSkillView(generics.DestroyAPIView):
    queryset = JobProfileSkill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Job Profile Skill deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a job profile skill.",
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Job Profile Skill deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

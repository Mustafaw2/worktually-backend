from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from job_seekers.modules.settings.models import Settings
from django.db import transaction
from job_seekers.pagination import CustomPageNumberPagination
from job_seekers.modules.job_profiles.models import JobProfile, JobProfilePortfolio
from django.shortcuts import get_object_or_404
from job_seekers.modules.job_profiles.serializers import (
    JobProfileSerializer,
    JobProfilePortfolioSerializer,
)


class GetJobProfileInfo(generics.ListAPIView):
    serializer_class = JobProfileSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        job_seeker = self.request.user
        # Add logging to verify the job_seeker and queryset
        if job_seeker:
            queryset = JobProfile.objects.filter(job_seeker=job_seeker)
            return queryset
        return JobProfile.objects.none()

    @swagger_auto_schema(
        operation_description="Get the completion rates of job profiles with pagination",
        responses={200: JobProfileSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "page_size",
                openapi.IN_QUERY,
                description="Number of items per page",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class JobProfileDetailView(APIView):
    @swagger_auto_schema(
        responses={200: JobProfileSerializer(), 400: "Bad Request", 404: "Not Found"}
    )
    def get(self, request, pk):
        try:
            job_profile = get_object_or_404(JobProfile, pk=pk)
            serializer = JobProfileSerializer(job_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except JobProfile.DoesNotExist:
            return Response(
                {"error": "Job profile not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AddJobProfileView(generics.CreateAPIView):
    queryset = JobProfile.objects.all()
    serializer_class = JobProfileSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobProfileSerializer,
        responses={
            201: openapi.Response(
                "Job Profile added successfully.", JobProfileSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a new job profile.",
    )
    def post(self, request, *args, **kwargs):
        # Check if the user has reached the profile limit
        try:
            profiles_limit = int(Settings.objects.get(key="profiles_limit").value)
        except Settings.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile limit setting not found."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        current_profile_count = JobProfile.objects.filter(
            job_seeker=request.user
        ).count()

        if current_profile_count >= profiles_limit:
            return Response(
                {
                    "status": "error",
                    "message": "You have reached the maximum number of job profiles.",
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                profile = serializer.save(job_seeker=request.user)
                return Response(
                    {"status": "success", "data": JobProfileSerializer(profile).data},
                    status=status.HTTP_201_CREATED,
                )
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateJobProfileView(generics.UpdateAPIView):
    queryset = JobProfile.objects.all()
    serializer_class = JobProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=JobProfileSerializer,
        responses={
            200: openapi.Response(
                "Job Profile updated successfully.", JobProfileSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing job profile.",
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            job_profile = serializer.save()
            return Response(
                {"status": "success", "data": JobProfileSerializer(job_profile).data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteJobProfileView(generics.DestroyAPIView):
    queryset = JobProfile.objects.all()
    serializer_class = JobProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Job Profile deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a job profile.",
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Job Profile deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class AddJobProfilePortfolioView(generics.CreateAPIView):
    queryset = JobProfilePortfolio.objects.all()
    serializer_class = JobProfilePortfolioSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobProfilePortfolioSerializer,
        responses={
            201: openapi.Response(
                "Portfolio added successfully.", JobProfilePortfolioSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a new job profile portfolio.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            portfolio = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": JobProfilePortfolioSerializer(portfolio).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateJobProfilePortfolioView(generics.UpdateAPIView):
    queryset = JobProfilePortfolio.objects.all()
    serializer_class = JobProfilePortfolioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=JobProfilePortfolioSerializer,
        responses={
            200: openapi.Response(
                "Portfolio updated successfully.", JobProfilePortfolioSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing job profile portfolio.",
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            portfolio = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": JobProfilePortfolioSerializer(portfolio).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteJobProfilePortfolioView(generics.DestroyAPIView):
    queryset = JobProfilePortfolio.objects.all()
    serializer_class = JobProfilePortfolioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Portfolio deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a job profile portfolio.",
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Portfolio deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
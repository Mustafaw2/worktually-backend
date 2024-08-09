from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from job_seekers.modules.experience.models import JobProfileExperience
from job_seekers.modules.experience.serializers import JobProfileExperienceSerializer


class AddExperienceView(generics.CreateAPIView):
    queryset = JobProfileExperience.objects.all()
    serializer_class = JobProfileExperienceSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=JobProfileExperienceSerializer,
        responses={
            201: openapi.Response(
                "Experience added successfully.", JobProfileExperienceSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a new job profile experience.",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            experience = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": JobProfileExperienceSerializer(experience).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UpdateExperienceView(generics.UpdateAPIView):
    queryset = JobProfileExperience.objects.all()
    serializer_class = JobProfileExperienceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        request_body=JobProfileExperienceSerializer,
        responses={
            200: openapi.Response(
                "Experience updated successfully.", JobProfileExperienceSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an existing job profile experience.",
    )
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            experience = serializer.save()
            return Response(
                {
                    "status": "success",
                    "data": JobProfileExperienceSerializer(experience).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": "error", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DeleteExperienceView(generics.DestroyAPIView):
    queryset = JobProfileExperience.objects.all()
    serializer_class = JobProfileExperienceSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    @swagger_auto_schema(
        responses={
            204: "Experience deleted successfully.",
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Delete a job profile experience.",
    )
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"status": "success", "message": "Experience deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

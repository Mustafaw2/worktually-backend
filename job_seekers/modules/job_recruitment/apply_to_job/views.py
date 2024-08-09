from rest_framework import generics, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import JobApplicationSerializer
from .models import JobApplication


class ApplyToJobView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer

    @swagger_auto_schema(
        operation_description="Apply for a job",
        request_body=JobApplicationSerializer,
        responses={
            201: openapi.Response(
                "Job application submitted successfully.", JobApplicationSerializer
            ),
            400: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Job application submitted successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

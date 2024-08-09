from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Education
from .serializers import EducationSerializer


class AddEducationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EducationSerializer,
        responses={
            201: openapi.Response("Education added successfully.", EducationSerializer),
            400: "Bad Request",
        },
        operation_description="Add an education entry.",
        examples={
            "application/json": {
                "job_seeker": 1,
                "title": "Bachelor of Science",
                "education_type_id": "BSc",
                "major_subjects": "Computer Science",
                "institute_name": "University of Example",
            }
        },
    )
    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Education added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateEducationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EducationSerializer,
        responses={
            200: openapi.Response(
                "Education updated successfully.", EducationSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update an education entry.",
        examples={
            "application/json": {
                "job_seeker": 1,
                "title": "Bachelor of Science",
                "education_type_id": "BSc",
                "major_subjects": "Computer Science",
                "score": "3.5 GPA",
                "completion_date": "2020-05-15",
                "institute_name": "University of Example",
                "certificate_photo": "path/to/certificate.jpg",
            }
        },
    )
    def put(self, request, pk):
        try:
            education = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response(
                {"status": "error", "message": "Education not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Education updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteEducationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Education deleted successfully.", 404: "Not Found"},
        operation_description="Delete an education entry.",
    )
    def delete(self, request, pk):
        try:
            education = Education.objects.get(pk=pk)
        except Education.DoesNotExist:
            return Response(
                {"status": "error", "message": "Education not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        education.delete()
        return Response(
            {"status": "success", "message": "Education deleted successfully"},
            status=status.HTTP_200_OK,
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import JobSeeker
from .serializers import BasicProfileSerializer
from rest_framework import generics, status
from worktually_v3_api.custom_jwt.jwt import JobSeekerJWTAuthentication


class JobSeekerDetailView(generics.RetrieveAPIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    queryset = JobSeeker.objects.all()
    serializer_class = BasicProfileSerializer
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response("Success", BasicProfileSerializer),
            404: "Not Found",
        },
        operation_description="Retrieve a job seeker's profile.",
    )
    def get(self, request, pk):
        try:
            profile = JobSeeker.objects.get(pk=pk)
        except JobSeeker.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(profile)
        return Response(
            {"status": "success", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class AddBasicProfileView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BasicProfileSerializer,
        responses={
            201: openapi.Response(
                "Profile added successfully.", BasicProfileSerializer
            ),
            400: "Bad Request",
        },
        operation_description="Add a basic profile.",
        examples={
            "application/json": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "birth_date": "1990-01-01",
                "gender": "Male",
                "country": "USA",
            }
        },
    )
    def post(self, request):
        serializer = BasicProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Profile added successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBasicProfileView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BasicProfileSerializer,
        responses={
            200: openapi.Response(
                "Profile updated successfully.", BasicProfileSerializer
            ),
            400: "Bad Request",
            404: "Not Found",
        },
        operation_description="Update a basic profile.",
        examples={
            "application/json": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "1234567890",
                "birth_date": "1990-01-01",
                "gender": "Male",
                "country": "USA",
            }
        },
    )
    def put(self, request, pk):
        try:
            profile = JobSeeker.objects.get(pk=pk)
        except JobSeeker.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BasicProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "Profile updated successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteBasicProfileView(APIView):
    authentication_classes = [JobSeekerJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: "Profile deleted successfully.", 404: "Not Found"},
        operation_description="Delete a basic profile.",
    )
    def delete(self, request, pk):
        try:
            profile = JobSeeker.objects.get(pk=pk)
        except JobSeeker.DoesNotExist:
            return Response(
                {"status": "error", "message": "Profile not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        profile.delete()
        return Response(
            {"status": "success", "message": "Profile deleted successfully"},
            status=status.HTTP_200_OK,
        )

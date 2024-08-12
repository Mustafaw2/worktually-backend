from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from job_seekers.modules.job_seeker.models import JobSeeker
from .serializers import JobSeekerSerializer, LoginSerializer, LogoutSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from .models import OTP
from .serializers import (
    ForgetPasswordSerializer,
    ResetPasswordRequestSerializer,
    VerifyOTPSerializer,
)
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=JobSeekerSerializer,
        responses={
            201: openapi.Response(
                description="User registered successfully",
                schema=JobSeekerSerializer,
                examples={
                    "application/json": {
                        "status": "success",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    }
                },
            ),
            400: "Bad Request",
        },
        operation_description="Register a new user.",
    )
    def post(self, request, format=None):
        serializer = JobSeekerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens for the registered user
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response(
                {
                    "status": "success",
                    "refresh": str(refresh),
                    "access": str(access),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    "application/json": {
                        "status": "success",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                    }
                },
            ),
            401: "Invalid email or password",
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            # Authenticate the user with email and password
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Generate tokens for the logged-in user
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "status": "success",
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                )
            else:
                return Response(
                    {"status": "error", "message": "Invalid email or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Logout successful",
                examples={
                    "application/json": {
                        "status": "success",
                    }
                },
            ),
        }
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            logout(request)
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ForgetPasswordSerializer,
        responses={200: "OTP has been sent to your email.", 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp_code = OTP.generate_otp()
            OTP.objects.create(email=email, otp=otp_code)
            send_mail(
                "Your OTP Code",
                f"Your OTP code is {otp_code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response(
                {"message": "OTP has been sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={
            200: "Success",
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp_instance = OTP.objects.get(
                email=serializer.validated_data["email"],
                otp=serializer.validated_data["otp"],
            )
            otp_instance.is_verified = True
            otp_instance.save()
            return Response(
                {
                    "message": "Success.",
                    "email": otp_instance.email,
                    "token": otp_instance.reset_token,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ResetPasswordRequestSerializer,
        responses={200: "Password reset successfully.", 400: "Bad Request"},
    )
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["new_password"]

            otp_instance = OTP.objects.filter(
                email=email, reset_token=token, is_verified=True
            ).first()
            if otp_instance:
                user = get_object_or_404(JobSeeker, email=email)
                user.set_password(new_password)
                user.save()
                otp_instance.delete()
                return Response(
                    {"message": "Success"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response({"message": "Provide your new password and token."})
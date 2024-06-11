from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from employee.models import Employee
from .serializers import RegisterSerializer, LoginSerializer, EmployeesSerializer, LogoutSerializer
from django.contrib.auth import authenticate, login, logout

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User registered successfully.', EmployeesSerializer),
            400: 'Bad Request'
        },
        operation_description="Register a new user.",
        examples={
            "application/json": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "password": "strong_password",
                "confirm_password": "strong_password",
                "phone": "1234567890",
            }
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(EmployeesSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                description="Login successful",
                examples={
                    'application/json': {
                        'message': 'Login successful',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                    }
                }
            ),
            401: "Invalid email or password",
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            # Authenticate the user with email and password
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Generate tokens for the logged-in user
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=LogoutSerializer,
        responses={
            200: "Logout successful",
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            logout(request)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

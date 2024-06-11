from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from drf_yasg.utils import swagger_auto_schema
from .models import Employee, BankAccount, EmergencyContact
from middlewares.role_permission_middleware import PermissionMiddleware
from django.contrib.auth import get_user_model
import json
import logging

logger = logging.getLogger(__name__)
UserProfile = get_user_model()
from drf_yasg import openapi
from .serializers import (
    EmployeeBasicSerializer,
    EmployeeWorkSerializer,
    EmployeeSerializer,
    EmployeePersonalSerializer,
    BankAccountSerializer,
    EmergencyContactSerializer,
    ChangeCoverPictureSerializer,
    ChangeProfilePictureSerializer
    
)

class EmployeesListView(APIView):
    def get(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmployeeSerializer,
        responses={201: EmployeeSerializer},
        operation_description="Add a new employee.",
        examples={
            "application/json": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "date_of_birth": "1990-01-01",
                "marital_status": "single",
                "gender": "male",
                "address": "123 Main St",
                "country": "USA",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90001",
                "emergency_contact": {
                    "name": "Jane Doe",
                    "relation": "sister",
                    "phone": "+123456789",
                    "email": "jane.doe@example.com",
                    "address": "456 Elm St"
                },
                "bank_account": {
                    "bank_name": "Bank of America",
                    "iban": "US123456789",
                    "account_name": "John Doe",
                    "bank_currency": "USD"
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        # Extract the JSON data
        data = request.data
        
        # Serialize the data
        serializer = EmployeeSerializer(data=data)
        
        # Validate and save the data
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Employee added successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        # If the data is not valid, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: EmployeeSerializer, 404: 'Employee not found.'},
        operation_description="Get detailed information of an employee by ID."
    )
    def get(self, request, employee_id):
        try:
            employee = Employee.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditBasicInformationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmployeeBasicSerializer,
        responses={
            200: openapi.Response('Basic information updated successfully.', EmployeeBasicSerializer),
            404: 'Employee not found.',
            400: 'Bad Request'
        },
        operation_description="Edit basic information of an employee by ID.",
        examples={
            "application/json": {
            "first_name": "Taha",
            "last_name": "Zaidi",
            "email": "taha@gmail.com",
            "phone": "123-456-7890",
            "father_name": "Michael Doe",
            "location_id": "LOC123"
            }
        }
    )
    def put(self, request, id, *args, **kwargs):
        try:
            employee = Employee.objects.get(id=id)
        except employee.DoesNotExist:
            return Response({"message": "employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeBasicSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Basic information updated successfully.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditWorkInformationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmployeeWorkSerializer,
        responses={
            200: openapi.Response('Work information updated successfully.', EmployeeWorkSerializer),
            404: 'Employee not found.',
            400: 'Bad Request'
        },
        operation_description="Edit work information of an employee by ID.",
        examples={
            'application/json': {
                'reporting_to': 1,
                'source_of_hiring': 'LinkedIn',
                'date_of_joining': '2022-01-01',
                'employee_type': 'Full-time',
                'exit_date': '2023-01-01',
                'status': 'Active'
            }
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeWorkSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Work information updated successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)


class EditPersonalInformationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmployeePersonalSerializer,
        responses={
            200: openapi.Response('Personal information updated successfully.', EmployeePersonalSerializer),
            404: 'Employee not found.',
            400: 'Bad Request'
        },
        operation_description="Edit personal information of an employee by ID.",
        examples={
            'application/json': {
                "first_name": "John",
                "email": "john.doe@example.com",
                "date_of_birth": "1990-01-01",
                "id_number": "A1234567",
                "marital_status": "Single",
                "gender": "Male",
                "address": "123 Main St, Springfield, IL, 62701"
            }
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeePersonalSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Personal information updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditBankAccountView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BankAccountSerializer,
        responses={
            200: openapi.Response('Bank account information updated successfully.', BankAccountSerializer),
            404: 'Employee not found.',
            400: 'Bad Request'
        },
        operation_description="Edit bank account information of an employee by ID.",
        examples={
            "application/json": {
                "bank_name": "Bank of America",
                "iban": "US123456789",
                "account_name": "John Doe",
                "bank_currency": "USD"
            }
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            bank_account = BankAccount.objects.get(pk=pk)
        except BankAccount.DoesNotExist:
            return Response({'error': 'Bank account not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = BankAccountSerializer(bank_account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Bank account information updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EditEmergencyInformationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmergencyContactSerializer,
        responses={
            200: openapi.Response('Emergency information updated successfully.'),
            404: 'Employee not found.',
            400: 'Bad Request'
        },
        operation_description="Edit emergency contact information of an employee by ID.",
        examples={
            "application/json": {
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "phone": "+11234567890",
                "relation": "Spouse",
                "address": "456 Elm St, Springfield, IL, 62702",
                "country_id": 1,
                "state_id": 1,
                "city_id": 1,
                "postal_code": "62702"
            }
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            emergency_contact = EmergencyContact.objects.get(pk=pk)
        except EmergencyContact.DoesNotExist:
            return Response({'error': 'Emergency contact not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmergencyContactSerializer(emergency_contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Emergency contact information updated successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ChangeProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=ChangeProfilePictureSerializer,
        responses={
            200: openapi.Response('Profile picture updated successfully.', ChangeProfilePictureSerializer),
            404: 'Employee not found.',
            400: 'Bad Request'
        },
        operation_description="Change profile picture of an employee by ID.",
        examples={
            "application/json": {
                "picture": "base64-encoded-image-string"
            }
        }
    )
    def put(self, request, pk, *args, **kwargs):
        logger.debug(f'Received request to change profile picture for employee id {pk}')
        logger.debug(f'Request data: {request.data}')
        logger.debug(f'Request FILES: {request.FILES}')
        print(request.FILES)

        try:
            employee = Employee.objects.get(pk=pk)
            logger.debug(f'Found employee: {employee}')
        except Employee.DoesNotExist:
            logger.error(f'Employee with id {pk} not found.')
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        logger.debug(f'Profile picture before update: {employee.picture}')

        if 'picture' in request.FILES:
            employee.picture = request.FILES['picture']
            employee.save()
            logger.debug(f'Profile picture after update: {employee.picture}')
            print(employee.picture)
            return Response({"message": "Profile picture changed successfully."}, status=status.HTTP_200_OK)
        else:
            logger.error('No picture found in request.')
            return Response({"message": "No picture found in request."}, status=status.HTTP_400_BAD_REQUEST)

class ChangeCoverPictureView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=ChangeCoverPictureSerializer,
        responses={
            200: openapi.Response('Cover picture updated successfully.', ChangeCoverPictureSerializer),
            404: 'Employee not found.',
            400: 'Bad Request'
        },
        operation_description="Change cover picture of an employee by ID.",
        examples={
            "application/json": {
                "cover_picture": "base64-encoded-image-string"
            }
        }
    )
    def put(self, request, pk, *args, **kwargs):
        logger.debug(f'Received request to change cover photo for employee id {pk}')
        logger.debug(f'Request data: {request.data}')
        logger.debug(f'Request FILES: {request.FILES}')

        try:
            employee = Employee.objects.get(pk=pk)
            logger.debug(f'Found employee: {employee}')
        except Employee.DoesNotExist:
            logger.error(f'Employee with id {pk} not found.')
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        logger.debug(f'Cover photo before update: {employee.cover_photo}')

        if 'cover_photo' in request.FILES:
            employee.cover_photo = request.FILES['cover_photo']
            employee.save()
            logger.debug(f'Cover photo after update: {employee.cover_photo}')
            return Response({"message": "Cover photo changed successfully."}, status=status.HTTP_200_OK)
        else:
            logger.error('No cover photo found in request.')
            return Response({"message": "No cover photo found in request."}, status=status.HTTP_400_BAD_REQUEST)

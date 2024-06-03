from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from authentication.models import User
from .models import UserProfile
from middlewares.role_permission_middleware import PermissionMiddleware
from django.contrib.auth import get_user_model
UserProfile = get_user_model()
from .serializers import (
    EmployeeBasicSerializer,
    EmployeeWorkSerializer,
    EmployeePersonalSerializer,
    EmployeeBankAccountSerializer,
    EmployeeEmergencySerializer,
    EmployeeSerializer,
    InviteEmployeeSerializer,
    ChangeProfilePictureSerializer,
    ChangeCoverPictureSerializer
)

class EmployeesListView(APIView):
    def get(self, request, *args, **kwargs):
        employees = UserProfile.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddEmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InviteEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_unusable_password()
            user.save()
            # Send invitation email here
            return Response({"message": "Employee invited successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, employee_id):
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EditBasicInformationView(APIView):
    permission_classes = [IsAuthenticated]

    

    def put(self, request, employee_id, *args, **kwargs):
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeBasicSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Basic information updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class EditWorkInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_id, *args, **kwargs):
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeWorkSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Work information updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditPersonalInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_id, *args, **kwargs):
        try:
            employee = UserProfile.objects.get(id=employee_id)
            print(employee)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeePersonalSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Personal information updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditBankAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_id, *args, **kwargs):
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeBankAccountSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Bank account information updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditEmergencyInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_id, *args, **kwargs):
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = EmployeeEmergencySerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Emergency information updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeProfilePictureView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_id, *args, **kwargs):
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeProfilePictureSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile picture updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeCoverPictureView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, employee_id, *args, **kwargs):
        try:
            employee = UserProfile.objects.get(id=employee_id)
        except UserProfile.DoesNotExist:
            return Response({"message": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ChangeCoverPictureSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Cover picture updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
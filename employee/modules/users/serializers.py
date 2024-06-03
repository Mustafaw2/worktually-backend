from rest_framework import serializers
from .models import UserProfile, EmergencyContact, BankAccount
from authentication.models import User


class EmployeeBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'father_name', 'date_of_birth', 'marital_status', 'gender', 'address', 'country', 'state', 'city', 'postal_code']


class EmployeeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['reporting_to', 'source_of_hiring', 'date_of_joining', 'employee_type', 'exit_date', 'status']

class EmployeePersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'email', 'date_of_birth', 'id_number', 'marital_status', 'gender', 'address']

class EmployeeBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['bank_name', 'iban', 'account_name', 'bank_currency']

class EmployeeEmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ['emergency_name', 'emergency_relation', 'emergency_phone', 'emergency_email', 'emergency_address']

class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserProfile
        fields = '__all__'

class InviteEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ChangeProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['picture']

class ChangeCoverPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['cover_photo']
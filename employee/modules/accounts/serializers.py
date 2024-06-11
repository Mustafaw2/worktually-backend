from rest_framework import serializers
from employee.models import Employee
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        # Remove confirm_password field
        confirm_password = validated_data.pop('confirm_password', None)
        
        # Create a new employee instance with the validated data
        employee = Employee.objects.create_user(**validated_data)
        return employee

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            print(user)
            if not user:
                raise serializers.ValidationError("Invalid email or password", code='authentication_failed')
        else:
            raise serializers.ValidationError("Both email and password are required", code='invalid_credentials')

        data['user'] = user
        return data

class EmployeesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'email', 'first_name', 'last_name', 'phone']

    
class LogoutSerializer(serializers.Serializer):
    pass

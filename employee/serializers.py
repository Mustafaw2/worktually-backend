from rest_framework import serializers
from .models import UserProfile, Experience, Dependent, Skill
from .modules.education_experience.serializers import EducationSerializer
from rest_framework import serializers
from .models import UserProfile, Role
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name', required=False)  # This allows inputting role as a string

    class Meta:
        model = UserProfile
        fields = [
            'user', 'first_name', 'last_name', 'father_name', 'email', 'date_of_birth', 'id_number', 
            'marital_status', 'gender', 'address', 'country', 'state', 'city', 'postal_code', 'picture', 
            'cover_photo', 'social_insurance_number', 'about', 'reporting_to', 'role', 'source_of_hiring', 
            'date_of_joining', 'employee_type', 'exit_date', 'status'
        ]

    def validate_role(self, role_name):
        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError(f"Role with name '{role_name}' does not exist.")
        return role

    def create(self, validated_data):
        role_name = validated_data.pop('role', None)
        user_profile = UserProfile.objects.create(**validated_data)
        if role_name:
            user_profile.role = self.validate_role(role_name['name'])
            user_profile.save()
        return user_profile

    def update(self, instance, validated_data):
        role_name = validated_data.pop('role', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if role_name:
            instance.role = self.validate_role(role_name['name'])
        instance.save()
        return instance



class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class DependentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependent
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

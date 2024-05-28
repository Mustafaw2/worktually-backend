from django.shortcuts import render

from rest_framework import generics
from .models import UserProfile, Education, Experience, Dependent, Skill
from .serializers import UserProfileSerializer, EducationSerializer, ExperienceSerializer, DependentSerializer, SkillSerializer
from .modules.education_experience.views import EditEducationView, AddEducationView, DeleteEducationView, EducationsListView

class EmployeesList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class AddEmployee(generics.CreateAPIView):
    serializer_class = UserProfileSerializer

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class EditBasicInformation(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class EditWorkInformation(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class EditPersonalInformation(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class EditBankAccount(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class EditEmergencyInformation(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ExperiencesList(generics.ListCreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class EditExperience(generics.RetrieveUpdateDestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

# class EducationsList(generics.ListCreateAPIView):
#     queryset = Education.objects.all()
#     serializer_class = EducationSerializer

# class EditEducation(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Education.objects.all()
#     serializer_class = EducationSerializer

class DependentsList(generics.ListCreateAPIView):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer

class EditDependent(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer

class SkillsList(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class DeleteSkill(generics.DestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ChangeProfilePicture(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class ChangeCoverPicture(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

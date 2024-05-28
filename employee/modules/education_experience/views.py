from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Education, Experience
from .serializers import EducationSerializer, ExperienceSerializer


class EducationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        educations = Education.objects.filter(user=request.user)
        serializer = EducationSerializer(educations, many=True)
        print(educations)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddEducationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Education added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditEducationView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, education_id):
        try:
            education = Education.objects.get(id=education_id, user=request.user)
        except Education.DoesNotExist:
            return Response({"message": "Education not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Education updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, education_id):
        try:
            education = Education.objects.get(id=education_id, user=request.user)
        except Education.DoesNotExist:
            return Response({"message": "Education not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Education updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteEducationView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, education_id):
        try:
            education = Education.objects.get(id=education_id, user=request.user)
        except Education.DoesNotExist:
            return Response({"message": "Education not found"}, status=status.HTTP_404_NOT_FOUND)

        education.delete()
        return Response({"message": "Your education has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    




from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Experience
from .serializers import ExperienceSerializer

class ExperiencesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        experiences = Experience.objects.filter(user=request.user)
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)

class AddExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Experience added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, experience_id):
        try:
            experience = Experience.objects.get(id=experience_id, user=request.user)
        except Experience.DoesNotExist:
            return Response({"message": "Experience not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExperienceSerializer(experience, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Experience updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, experience_id):
        try:
            experience = Experience.objects.get(id=experience_id, user=request.user)
        except Experience.DoesNotExist:
            return Response({"message": "Experience not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Experience updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteExperienceView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, experience_id):
        try:
            experience = Experience.objects.get(id=experience_id, user=request.user)
        except Experience.DoesNotExist:
            return Response({"message": "Experience not found"}, status=status.HTTP_404_NOT_FOUND)

        experience.delete()
        return Response({"message": "Your experience has been deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
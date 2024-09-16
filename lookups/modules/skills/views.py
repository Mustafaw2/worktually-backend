from rest_framework import generics
from lookups.models import SkillCategory
from .serializers import SkillCategorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class SkillCategoryListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        skill_categories = SkillCategory.objects.all()
        serializer = SkillCategorySerializer(skill_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
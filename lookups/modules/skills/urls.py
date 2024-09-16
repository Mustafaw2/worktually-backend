from django.urls import path
from .views import SkillCategoryListAPIView

urlpatterns = [
    path('skill-categories/', SkillCategoryListAPIView.as_view(), name='skill-category-list'),
]
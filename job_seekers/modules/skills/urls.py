from django.urls import path
from job_seekers.modules.skills.views import *
from lookups.models import SkillCategory

urlpatterns = [
    path("category/add/", AddSkillCategoryView.as_view(), name="add_skill_category"),
    path(
        "category/update/<int:pk>/",
        UpdateSkillCategoryView.as_view(),
        name="update_skill_category",
    ),
    path(
        "category/delete/<int:pk>/",
        DeleteSkillCategoryView.as_view(),
        name="delete_skill_category",
    ),
    path("add/", AddSkillsToJobProfileView.as_view(), name="add_skill"),
    path("update/<int:pk>/", UpdateSkillView.as_view(), name="update_skill"),
    path("delete/<int:pk>/", DeleteSkillView.as_view(), name="delete_skill"),
    path(
        "job_profile_skill/add/",
        AddJobProfileSkillView.as_view(),
        name="add_job_profile_skill",
    ),
    path(
        "job_profile_skill/update/<int:pk>/",
        UpdateJobProfileSkillView.as_view(),
        name="update_job_profile_skill",
    ),
    path(
        "job_profile_skill/delete/<int:pk>/",
        DeleteJobProfileSkillView.as_view(),
        name="delete_job_profile_skill",
    ),
]

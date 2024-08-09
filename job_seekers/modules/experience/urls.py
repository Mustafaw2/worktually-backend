from django.urls import path
from job_seekers.modules.experience.views import (
    AddExperienceView,
    UpdateExperienceView,
    DeleteExperienceView,
)

urlpatterns = [
    path("add/", AddExperienceView.as_view(), name="add_experience"),
    path("update/<int:pk>/", UpdateExperienceView.as_view(), name="update_experience"),
    path("delete/<int:pk>/", DeleteExperienceView.as_view(), name="delete_experience"),
]

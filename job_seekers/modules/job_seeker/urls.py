from django.urls import path
from .views import (
    AddBasicProfileView,
    UpdateBasicProfileView,
    DeleteBasicProfileView,
    JobSeekerDetailView,
)

urlpatterns = [
    path("add/", AddBasicProfileView.as_view(), name="add_profile"),
    path(
        "update/<int:pk>/",
        UpdateBasicProfileView.as_view(),
        name="update_profile",
    ),
    path(
        "delete/<int:pk>/",
        DeleteBasicProfileView.as_view(),
        name="delete_profile",
    ),
    path("<int:pk>/", JobSeekerDetailView.as_view(), name="job-seeker-detail"),
]

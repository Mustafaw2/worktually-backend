from django.urls import path
from .views import (
    AddBasicProfileView,
    UpdateBasicProfileView,
    DeleteBasicProfileView,
    JobSeekerDetailView,
    ValidateTokenView
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
    path("info/", JobSeekerDetailView.as_view(), name="job-seeker-detail"),
    path('validate-token/', ValidateTokenView.as_view(), name='validate-token'),
]

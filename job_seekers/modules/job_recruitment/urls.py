from django.urls import path
from .views import JobPostListView

urlpatterns = [
    path("job-posts/", JobPostListView.as_view(), name="job_post_list"),
]

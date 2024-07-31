from django.urls import path
from .views import JobPostCreateView, JobPostEditView, JobPostDeleteView, JobPostDetailView, JobPostListView

urlpatterns = [
    path('job-posts/add', JobPostCreateView.as_view(), name='job-post-create'),
    path('job-posts/edit/<int:pk>/', JobPostEditView.as_view(), name='job-post-edit'),
    path('job-posts/delete/<int:pk>/', JobPostDeleteView.as_view(), name='job-post-delete'),
    path('job-posts/<int:pk>/', JobPostDetailView.as_view(), name='job-post-detail'),
    path('job-posts/list/', JobPostListView.as_view(), name='job_post_list'),
]
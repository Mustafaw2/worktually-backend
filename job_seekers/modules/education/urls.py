from django.urls import path
from .views import AddEducationView, UpdateEducationView, DeleteEducationView

urlpatterns = [
    path("add/", AddEducationView.as_view(), name="add_education"),
    path("update/<int:pk>/", UpdateEducationView.as_view(), name="update_education"),
    path("delete/<int:pk>/", DeleteEducationView.as_view(), name="delete_education"),
]

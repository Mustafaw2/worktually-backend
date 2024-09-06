from django.urls import path
from .views import AddEducationView, UpdateEducationView, DeleteEducationView

urlpatterns = [
    path("add/", AddEducationView.as_view(), name="add_education"),
    path("update/", UpdateEducationView.as_view(), name="update_education"),
    path("delete/", DeleteEducationView.as_view(), name="delete_education"),
]


from django.urls import path
from .views import AddLanguageView, UpdateLanguageView, DeleteLanguageView

urlpatterns = [
    path("add/", AddLanguageView.as_view(), name="add_language"),
    path("update/", UpdateLanguageView.as_view(), name="update_language"),
    path("delete/", DeleteLanguageView.as_view(), name="delete_language"),
]

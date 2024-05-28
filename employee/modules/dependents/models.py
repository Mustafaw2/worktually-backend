from django.db import models
from employee.modules.users.models import UserProfile
from django.conf import settings

class Dependent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=100)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    social_insurance_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relation})"

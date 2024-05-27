from django.db import models
from django.conf import settings

class Role(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_roles')

    def __str__(self):
        return self.name

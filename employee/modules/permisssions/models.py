from django.db import models

class PermissionModule(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Permission(models.Model):
    module = models.ForeignKey(PermissionModule, on_delete=models.CASCADE, related_name='permissions')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
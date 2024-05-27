from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='organization/logos/', blank=True, null=True)
    industry = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Location(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    currency = models.CharField(max_length=3)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    logo = models.ImageField(upload_to='locations/logos/', blank=True, null=True)

    def __str__(self):
        return self.name
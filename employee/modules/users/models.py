from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    id_number = models.CharField(max_length=50, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    social_insurance_number = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    reporting_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    source_of_hiring = models.CharField(max_length=100, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    employee_type = models.CharField(max_length=50, blank=True, null=True)
    exit_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Active', 'Active'), ('Resigned', 'Resigned'), ('Terminated', 'Terminated'), ('Suspended', 'Suspended')], default='Active')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.email}"
    

class EmergencyContact(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='emergency_contact')
    name = models.CharField(max_length=100, blank=True, null=True)
    relation = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.relation})"

class BankAccount(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='bank_account')
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    iban = models.CharField(max_length=34, blank=True, null=True)
    account_name = models.CharField(max_length=100, blank=True, null=True)
    bank_currency = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.bank_name
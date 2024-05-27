from django.db import models

class Lookup(models.Model):
    CATEGORY_CHOICES = [
        ('Industry', 'Industry'),
        ('Country', 'Country'),
        ('State', 'State'),
        ('City', 'City'),
        ('Designation', 'Designation'),
        ('Department', 'Department'),
        ('Source', 'Source'),
        ('DegreeType', 'Degree Type'),
        ('EmployeeType', 'Employee Type'),
        ('JobType', 'Job Type'),
        ('Relation', 'Relation'),
        ('Skill', 'Skill'),
        ('Language', 'Language'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='Active')
    iso3 = models.CharField(max_length=100, null=True, blank=True)
    iso2 = models.CharField(max_length=100, null=True, blank=True)
    phone_code = models.CharField(max_length=100, null=True, blank=True)
    capital = models.CharField(max_length=255, null=True, blank=True)
    currency = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
from django.db import models

class Industry(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_industry'
        app_label = 'lookups'

from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, default='')
    iso3 = models.CharField(max_length=3, default='')
    iso2 = models.CharField(max_length=2, default='')
    phone_code = models.CharField(max_length=20, default='')
    capital = models.CharField(max_length=255, default='')
    currency = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'lookup_country'
        app_label = 'lookups'

class State(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        db_table = 'lookup_state'
        app_label = 'lookups'

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    class Meta:
        db_table = 'lookup_city'
        app_label = 'lookups'

class Designation(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_designation'
        app_label = 'lookups'

class Department(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_department'
        app_label = 'lookups'

class Source(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_source'
        app_label = 'lookups'

class DegreeType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_degree_type'
        app_label = 'lookups'

class EmployeeType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_employee_type'
        app_label = 'lookups'

class JobType(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_job_type'
        app_label = 'lookups'

class Relation(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_relation'
        app_label = 'lookups'

class Skill(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_skill'
        app_label = 'lookups'

class Language(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)

    class Meta:
        db_table = 'lookup_language'
        app_label = 'lookups'

from django.db import models

class JobSeeker(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(max_length=45)
    password = models.CharField(max_length=45)
    phone = models.CharField(max_length=45)
    father_name = models.CharField(max_length=45)
    source_id = models.IntegerField()
    status = models.CharField(max_length=45)
    birth_date = models.DateField()
    id_number = models.CharField(max_length=45)
    marital_status = models.CharField(max_length=45)
    gender = models.CharField(max_length=45)
    picture = models.CharField(max_length=45)
    cover_photo = models.CharField(max_length=45)
    about = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
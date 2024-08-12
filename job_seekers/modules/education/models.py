from django.db import models
from django.apps import apps


class Education(models.Model):
    job_seeker = models.ForeignKey(
        "job_seekers.JobSeeker", on_delete=models.CASCADE, related_name="Education"
    )
    title = models.CharField(max_length=45)
    education_type_id = models.CharField(max_length=45)
    major_subjects = models.CharField(max_length=45)
    score = models.CharField(max_length=45)
    completion_date = models.DateField(null=True, blank=True)
    institute_name = models.CharField(max_length=45)
    certificate_photo = models.CharField(max_length=45)

    class Meta:
        app_label = 'job_seekers'

    def __str__(self):
        return self.title

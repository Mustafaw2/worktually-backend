from django.db import models
from django.apps import apps


class JobProfileExperience(models.Model):
    job_seeker = models.ForeignKey(
        "job_seekers.JobSeeker",
        on_delete=models.CASCADE,
        related_name="jobprofile_experiences",
    )
    title = models.CharField(max_length=45)
    job_type_id = models.CharField(max_length=45)
    company_name = models.CharField(max_length=45)
    start_date = models.DateField()
    currently_working = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=45)
    experience_letter_photo = models.CharField(max_length=45)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return self.title

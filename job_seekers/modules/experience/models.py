from django.db import models
from django.utils import timezone
from lookups.models import Country, City

class JobProfileExperience(models.Model):
    job_seeker = models.ForeignKey(
        "job_seekers.JobSeeker",
        on_delete=models.CASCADE,
        related_name="jobprofile_experiences",
    )
    company_name = models.CharField(max_length=45)
    start_date = models.DateField()
    currently_working = models.BooleanField(default=False)
    end_date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=45)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True, related_name="experiences"
    )
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, null=True, blank=True, related_name="experiences"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return f"{self.company_name} - {self.job_seeker}"

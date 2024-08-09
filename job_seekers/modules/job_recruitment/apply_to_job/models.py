from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from job_seekers.models import JobProfile, JobSeeker


class JobApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        SHORTLISTED = "shortlisted", _("Shortlisted")
        REJECTED = "rejected", _("Rejected")

    job_id = models.IntegerField()
    job_seeker = models.ForeignKey(
        JobSeeker, on_delete=models.CASCADE, related_name="applications"
    )
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name="applications"
    )
    date_applied = models.DateTimeField(default=timezone.now)
    source = models.CharField(max_length=255)
    is_applied = models.BooleanField(default=False)
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        app_label = "job_seekers"

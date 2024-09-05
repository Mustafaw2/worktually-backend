from datetime import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class JobProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        REJECTED = "rejected", _("Rejected")
        APPROVED = "approved", _("Approved")

    job_seeker = models.ForeignKey(
        "job_seekers.JobSeeker",
        on_delete=models.CASCADE,
        null=True,
        related_name="job_profile",
    )
    job_title = models.ForeignKey(
        "lookups.JobTitle",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="job_profiles",
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    completion_rate = models.IntegerField(null=True, blank=True)
    priority = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    
    reviewed_at = models.CharField(max_length=45)
    rating = models.CharField(max_length=45)
    is_approved = models.BooleanField(default=False)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return f"Job Profile {self.id} - {self.job_title}"

    def sync_completion_rate(self):
        # Sync completion_rate from JobSeeker's profile_completion_percentage
        if self.job_seeker:
            self.completion_rate = int(
                self.job_seeker.approval.profile_completion_percentage
            )
            self.save()

    def sync_is_approved(self):
        # Sync is_approved from JobSeeker's is_approved
        if self.job_seeker:
            self.is_approved = self.job_seeker.approval.is_approved
            self.save()


class JobProfileReview(models.Model):
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name="reviews"
    )
    communication_rating = models.FloatField()
    experience_rating = models.FloatField()
    education_rating = models.FloatField()
    skills_rating = models.FloatField()
    comments = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    reject_reason_id = models.IntegerField()
    next_review = models.DateField()
    # reviewed_by = models.IntegerField()

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return self.comments


class JobProfilePortfolio(models.Model):
    job_profile = models.ForeignKey(
        JobProfile, on_delete=models.CASCADE, related_name="portfolios"
    )
    project_title = models.CharField(max_length=45)
    description = models.TextField()
    url = models.CharField(max_length=45)
    files = models.FileField(upload_to='portfolios/')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return self.project_title

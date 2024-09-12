from datetime import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from job_seekers.modules.job_seeker.models import ApprovalModel


class JobProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        REJECTED = "rejected", _("Rejected")
        APPROVED = "approved", _("Approved")

    job_seeker = models.ForeignKey('job_seekers.JobSeeker', on_delete=models.CASCADE, related_name="job_profile")
    job_title = models.ForeignKey(
        "lookups.JobTitle",
        on_delete=models.CASCADE,
        null=True,
        default=None,
        related_name="job_profiles",
    )
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    completion_rate = models.IntegerField(default=0)
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
        # Step 1: Fetch the base completion rate from the ApprovalModel
        approval = ApprovalModel.objects.get(job_seeker=self.job_seeker)
        base_completion_rate = approval.profile_completion_percentage
        print(f"Base completion rate from ApprovalModel: {base_completion_rate}")

        # Step 2: Calculate experience and skills points
        experience_points = self.calculate_experience_points()
        print(f"Experience points for JobProfile {self.id}: {experience_points}")

        skills_points = self.calculate_skills_points()
        print(f"Skills points for JobProfile {self.id}: {skills_points}")

        portfolio_points = self.calculate_portfolio_points()
        print(f"Portfolio points for JobProfile {self.id}: {portfolio_points}")

        # Step 3: Add experience points (23%), skills points, and portfolio points to the base completion rate
        updated_completion_rate = base_completion_rate + experience_points + skills_points + portfolio_points
        print(f"Final completion rate for JobProfile {self.id}: {updated_completion_rate}")

        # Step 4: Ensure the updated completion rate does not exceed 100%
        self.completion_rate = min(updated_completion_rate, 100)
        self.save()

        self.completion_rate = updated_completion_rate
        if updated_completion_rate >= 90:
            self.status = self.STATUS_APPROVED
        else:
            self.status = self.STATUS_PENDING
        
        self.save()

    def calculate_experience_points(self):
        """Calculate experience points, which are 23% of the completion rate."""
        experience_points = 23  # 23% for adding experience
        return experience_points

    def calculate_skills_points(self):
        """Calculate skills points, which are 23% of the completion rate."""
        # Add 23 points for having skills in this profile
        skills_points = 23 if self.job_profile_skills.exists() else 0
        return skills_points
    

    def calculate_portfolio_points(self):
        """Calculate portfolio points, which are 23% of the completion rate."""
        return 23 if self.portfolios.exists() else 0




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
    url = models.CharField(max_length=255)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return self.project_title

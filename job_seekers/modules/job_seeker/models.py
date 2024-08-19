from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db import transaction


class JobSeekerManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name, last_name=last_name, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, first_name, last_name, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, first_name, last_name, password, **extra_fields)


class JobSeeker(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    phone = models.CharField(max_length=45, blank=True)
    father_name = models.CharField(max_length=45, blank=True)
    source_id = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=45, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=45, blank=True)
    marital_status = models.CharField(max_length=45, blank=True)
    gender = models.CharField(max_length=45, blank=True)
    profile_picture = models.CharField(max_length=45, blank=True)
    cover_photo = models.CharField(max_length=45, blank=True)
    about = models.TextField(blank=True)
    country = models.CharField(max_length=45, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = JobSeekerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        indexes = [
            models.Index(fields=["id"]),
        ]

    class Meta:
        app_label = "job_seekers"

    # Add related_name to avoid clashes with default User model
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="job_seeker_set",
        blank=True,
        help_text="The groups this user belongs to.",
        related_query_name="job_seeker",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="job_seeker_set",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="job_seeker",
    )

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_staff

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_staff

    def get_profile_completion(self):
        approval = ApprovalModel.objects.get(job_seeker=self)
        return approval.profile_completion_percentage

    def update_profile_completion(self):
        print(f"Updating profile completion for JobSeeker {self.id}")

        # Calculate profile picture points
        profile_picture_points = 0.25 if self.profile_picture else 0
        print(f"Profile picture points: {profile_picture_points}")

        # Calculate education points
        education_points = 1 if self.Education.exists() else 0
        print(f"Education points: {education_points}")

        # Calculate languages points
        languages_points = 1 if self.language.exists() else 0
        print(f"Languages points: {languages_points}")

        # Calculate experience points
        experience_points = 1 if self.jobprofile_experiences.exists() else 0
        print(f"Experience points: {experience_points}")

        # Calculate skills score points
        skills_score_points = self.calculate_skills_score()
        print(f"Skills score points: {skills_score_points}")

        # Calculate total points and profile completion percentage
        total_points = (
            profile_picture_points
            + education_points
            + languages_points
            + experience_points
            + skills_score_points
        )
        profile_completion_percentage = (total_points / 4.25) * 100
        print(f"Profile completion percentage: {profile_completion_percentage}")

        # Update or create ApprovalModel instance
        with transaction.atomic():
            approval, created = ApprovalModel.objects.get_or_create(job_seeker=self)
            approval.profile_completion_percentage = profile_completion_percentage
            approval.update_approval_status()
            approval.save()

        # Update associated job profiles
        for profile in self.job_profile.all():
            profile.sync_completion_rate()
            profile.sync_is_approved()

    def calculate_skills_score(self):
        job_profiles = self.job_profile.all()
        total_skills = sum(
            profile.job_profile_skills.count() for profile in job_profiles
        )
        print(f"Total skills: {total_skills}")
        return 1 if total_skills > 0 else 0


class ApprovalModel(models.Model):
    job_seeker = models.OneToOneField(
        JobSeeker, on_delete=models.CASCADE, related_name="approval"
    )
    profile_completion_percentage = models.FloatField(default=0)
    is_approved = models.BooleanField(default=False)

    def update_approval_status(self):
        if self.profile_completion_percentage >= 90:
            self.is_approved = True
        else:
            self.is_approved = False
        self.save()

    class Meta:
        app_label = "job_seekers"

    def __str__(self):
        return f"Approval for {self.job_seeker.first_name} {self.job_seeker.last_name}"

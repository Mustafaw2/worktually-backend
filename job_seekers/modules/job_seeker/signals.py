from django.db.models.signals import post_save
from django.dispatch import receiver

from recruitment.models import Candidate, JobApplication

from job_seekers.models import (
    JobSeeker,
    Education,
    Language,
    JobProfileExperience,
    Skills,
    JobProfilePortfolio,
    JobProfileSkill,
)


@receiver(post_save, sender=Education)
def update_profile_completion_on_education_save(sender, instance, **kwargs):
    print("Education updated, updating profile completion")
    instance.job_seeker.update_profile_completion()


@receiver(post_save, sender=Language)
def update_profile_completion_on_language_save(sender, instance, **kwargs):
    print("Language updated, updating profile completion")
    instance.job_seeker.update_profile_completion()



@receiver(post_save, sender=JobProfileExperience)
def update_profile_completion_on_experience_save(sender, instance, **kwargs):
    print("Experience updated, updating profile completion")
    # Update completion rate only for the specific job profile associated with the experience
    instance.job_profile.sync_completion_rate()




@receiver(post_save, sender=JobProfileSkill)
def update_profile_completion_on_skill_save(sender, instance, **kwargs):
    print("JobProfileSkill updated, updating profile completion")
    # Update completion rate only for the specific job profile associated with the skill
    instance.job_profile.sync_completion_rate()

@receiver(post_save, sender=JobProfilePortfolio)
def update_job_profile_completion_rate(sender, instance, **kwargs):
    # Ensure that the completion rate is updated when a portfolio is added or updated
    instance.job_profile.sync_completion_rate()


@receiver(post_save, sender=JobApplication)
def create_candidate(sender, instance, created, **kwargs):
    if created:
        Candidate.objects.create(
            job_application_id=instance,
            job_profile_id=instance.job_profile,  # Assuming job_profile is a field in JobApplication
            job_seeker_id=instance.job_seeker,  # Assuming job_seeker is a field in JobApplication
            status="Applied",  # Set default status or update as needed
            expected_start_date=None,  # Set default value or leave it to be updated later
        )

from django.db.models.signals import post_save
from django.dispatch import receiver
from ....models import JobApplication
from job_seekers.models import Candidate


@receiver(post_save, sender=JobApplication)
def create_candidate(sender, instance, created, **kwargs):
    if created:
        Candidate.objects.create(
            job_application_id=instance,  # Use job_application_id instead of job_application
            status="Applied",  # Set default status or update as needed
            expected_start_date=None,  # Set default value or leave it to be updated later
        )

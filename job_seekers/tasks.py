from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import JobApplication, JobSeeker
import requests
import os
from dotenv import load_dotenv
from .email_templates import (
    get_job_application_email_subject,
    get_job_application_email_body,
)

load_dotenv()


@shared_task
def send_job_application_notification(job_application_id):
    # Fetch API key from environment variables
    api_key = os.getenv("API_KEY")
    headers = {"Authorization": f"Api-Key {api_key}"}

    # Get job application details
    job_application = JobApplication.objects.get(id=job_application_id)
    job_post_id = job_application.job_id

    # Get job post details from the employee project
    job_post_response = requests.get(
        f"http://localhost:8000/api/recruitment/job-posts/{job_post_id}/",
        headers=headers,
    )
    if job_post_response.status_code != 200:
        raise Exception("Job post not found")
    job_post = job_post_response.json()["data"]

    # Fetch organization details using the organization ID from the job post
    organization_id = job_post["organization_id"]
    organization_response = requests.get(
        f"http://localhost:8000/api/organizations/{organization_id}/",
        headers=headers,
    )

    if organization_response.status_code != 200:
        raise Exception("Organization not found")

    organization = organization_response.json()["data"]

    organization_email = organization["email"]

    # Fetch job seeker details from the local database
    job_seeker_id = job_application.job_seeker.id
    try:
        job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    except JobSeeker.DoesNotExist:
        raise Exception("Job seeker not found")

    # Send email notification
    subject = get_job_application_email_subject()
    body = get_job_application_email_body(
        organization, job_post, job_seeker, job_application
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [organization_email],
        fail_silently=False,
    )

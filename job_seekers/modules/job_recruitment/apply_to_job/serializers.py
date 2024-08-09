import os
import requests
from rest_framework import serializers
from .models import JobApplication, JobProfile
from job_seekers.tasks import send_job_application_notification


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["job_id", "job_seeker", "job_profile", "source", "status"]

    def validate_job_post(self, value):
        api_key = os.getenv("API_KEY")
        headers = {"Authorization": f"Api-Key {api_key}"}

        # Fetch the list of job posts
        response = requests.get(
            "https://dev3-api.worktually.com/api/recruitment/job-posts/list/",
            headers=headers,
        )

        if response.status_code != 200:
            raise serializers.ValidationError("Unable to fetch job posts.")

        job_posts_data = response.json()
        job_posts = job_posts_data.get("data", [])

        # Extract all job post IDs from the response
        job_post_ids = [job_post["id"] for job_post in job_posts]

        if value not in job_post_ids:
            raise serializers.ValidationError("Job post does not exist.")

        return value

    def validate_job_profile(self, value):
        if not JobProfile.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Job profile does not exist.")
        return value

    def validate(self, data):
        # Validate job post ID
        job_post_id = data.get("job_id")
        if job_post_id:
            self.validate_job_post(job_post_id)

        # Validate job profile ID
        job_profile_id = data.get("job_profile")
        if job_profile_id:
            self.validate_job_profile(job_profile_id)

        return data

    def create(self, validated_data):
        # Create the job application instance
        job_application = super().create(validated_data)

        send_job_application_notification.delay(job_application.id)

        # Update the 'is_applied' field to True
        job_application.is_applied = True
        job_application.save()

        return job_application

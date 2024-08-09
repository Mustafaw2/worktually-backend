from rest_framework import serializers
from .models import JobApplication, JobProfile
import os
import requests


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["job_seeker", "job_post", "job_profile", "source"]

    def validate_job_post(self, value):
        api_key = os.getenv("RECRUITMENT_API_KEY")
        headers = {"Authorization": f"Api-Key {api_key}"}

        # Fetch the list of job posts
        response = requests.get(
            "http://localhost:8000/api/recruitment/job-posts/list/", headers=headers
        )

        if response.status_code != 200:
            raise serializers.ValidationError("Unable to fetch job posts.")

        job_posts_data = response.json()
        job_posts = job_posts_data.get("data", [])

        # Extract all job post IDs from the response
        job_post_ids = [job_post["id"] for job_post in job_posts]
        print(job_post_ids)

        if value not in job_post_ids:
            raise serializers.ValidationError("Job post does not exist.")

        return value

    def validate_job_profile(self, value):
        if not JobProfile.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Job profile does not exist.")
        return value

    def validate(self, data):
        data["job_post"] = self.validate_job_post(data.get("job_post"))
        data["job_profile"] = self.validate_job_profile(data.get("job_profile"))
        return data

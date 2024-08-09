import requests
from rest_framework import serializers
import os


class JobSearchSerializer(serializers.Serializer):
    job_title_id = serializers.IntegerField()

    def validate_job_title_id(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Job title ID must be a positive integer."
            )
        return value

    def search_jobs(self, job_title_id):
        job_title_id = self.validated_data.get("job_title_id")
        api_key = os.getenv("API_KEY")
        headers = {"Authorization": f"Api-Key {api_key}"}

        response = requests.get(
            "https://dev3-api.worktually.com/api/recruitment/job-posts/list/",
            headers=headers,
        )

        if response.status_code != 200:
            raise serializers.ValidationError("Unable to fetch job posts.")

        job_posts_data = response.json()
        job_posts = job_posts_data.get("data", [])

        filtered_job_posts = [
            job_post
            for job_post in job_posts
            if job_post["job_title_id"] == job_title_id
        ]

        if not filtered_job_posts:
            raise serializers.ValidationError(
                "No job posts found for the given job title ID."
            )

        return filtered_job_posts

from rest_framework import serializers
from recruitment.models import JobOffer
import os
import requests

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ['job_post_id', 'candidate_id', 'currency', 'amount', 'counter_amount', 'counter_by', 'expired_at']

    def validate_candidate_id(self, value):
        # Assuming the candidate API is hosted at http://localhost:8001/api/candidates/{id}/
        api_key = os.getenv('API_KEY')
        headers = {'Authorization': f'Api-Key {api_key}'}
        response = requests.get(f'http://localhost:8001/api/candidates/{value}/', headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError("Candidate does not exist.")
        return value

    def validate_job_post_id(self, value):
        # Assuming the job post API is hosted at http://localhost:8000/api/recruitment/job-posts/{id}/
        api_key = os.getenv('API_KEY')
        headers = {'Authorization': f'Api-Key {api_key}'}
        response = requests.get(f'http://localhost:8000/api/recruitment/job-posts/{value}/', headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError("Job post does not exist.")
        return value

    def validate(self, data):
        # Custom validation logic if needed
        return data

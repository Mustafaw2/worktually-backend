import requests
import os
from datetime import date
from rest_framework import serializers
from recruitment.models import JobOffer, JobPost

class HireCandidateSerializer(serializers.Serializer):
    job_post_id = serializers.IntegerField()
    candidate_id = serializers.IntegerField()
    job_offer_id = serializers.IntegerField()
    hire_date = serializers.DateField()

    def validate_job_post_id(self, value):
        try:
            JobPost.objects.get(id=value)
        except JobPost.DoesNotExist:
            raise serializers.ValidationError("Job post does not exist.")
        return value

    def validate_candidate_id(self, value):
        api_key = os.getenv('API_KEY')
        url = f"https://seekerdev3-api.worktually.com/api/candidates/{value}/"
        headers = {'Authorization': f'Api-Key {api_key}'}
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise serializers.ValidationError("Candidate does not exist.")
        
        return value

    def validate(self, data):
        job_offer_id = data.get('job_offer_id')
        try:
            job_offer = JobOffer.objects.get(id=job_offer_id)
            if job_offer.status != "Accept":
                raise serializers.ValidationError("The job offer is not accepted.")
        except JobOffer.DoesNotExist:
            raise serializers.ValidationError("Job offer does not exist.")
        
        data['job_offer'] = job_offer
        return data

    def validate_hire_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Hire date cannot be in the past.")
        return value


    def create(self, validated_data):
        job_post_id = validated_data['job_post_id']
        candidate_id = validated_data['candidate_id']
        job_offer_id = validated_data['job_offer_id']
        hire_date = validated_data['hire_date']

        # Update candidate status to 'Hired'
        url = f"https://seekerdev3-api.worktually.com/api/candidates/{candidate_id}/"
        headers = {'Authorization': f'Api-Key {os.getenv("API_KEY")}'}
        response = requests.get(url, headers=headers)
        candidate_response = response.json()
        candidate_data = candidate_response.get('data', {})
        candidate_data['status'] = 'Hired'
        update_response = requests.patch(url, headers=headers, json=candidate_data)
        if update_response.status_code != 200:
            raise serializers.ValidationError("Failed to update candidate status.")

        # Return the validated data or any other relevant information
        return {
            "job_post_id": job_post_id,
            "candidate_id": candidate_id,
            "job_offer_id": job_offer_id,
            "hire_date": hire_date,
            "status": candidate_data['status']
        }


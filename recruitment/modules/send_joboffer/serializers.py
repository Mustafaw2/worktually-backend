import os
import requests
from rest_framework import serializers
from recruitment.models import JobOffer
from recruitment.tasks import send_job_offer_notification

class JobOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOffer
        fields = [
            "job_post_id",
            "candidate_id",
            "currency",
            "amount",
            "counter_amount",
            "counter_by",
            "expired_at"
        ]

    def validate_candidate_id(self, value):
        api_key = os.getenv('API_KEY')
        candidates_api_url = f"https://seekerdev3-api.worktually.com/api/candidates/{value}/"
        headers = {'Authorization': f'Api-Key {api_key}'}
        
        response = requests.get(candidates_api_url, headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError("Invalid candidate ID.")

        candidate_response = response.json()
        candidate_data = candidate_response.get('data', {})
        
        if not candidate_data:
            raise serializers.ValidationError("Candidate data not found.")

        job_seeker_id = candidate_data.get('job_seeker_id')
        if not job_seeker_id:
            raise serializers.ValidationError("Job seeker ID not found in candidate data.")
        
        # Attach job_seeker_id to the serializer context for later use
        self.context['job_seeker_id'] = job_seeker_id
        
        return value

    def create(self, validated_data):
        job_offer = super().create(validated_data)
        api_key = os.getenv('API_KEY')
        job_seeker_id = self.context['job_seeker_id']
        job_seeker_api_url = f"https://seekerdev3-api.worktually.com/api/job_seeker/list/{job_seeker_id}/"
        headers = {'Authorization': f'Api-Key {api_key}'}
        
        response = requests.get(job_seeker_api_url, headers=headers)
        if response.status_code == 200:
            job_seeker_response = response.json()
            job_seeker_data = job_seeker_response.get('data', {})
            if not job_seeker_data:
               raise serializers.ValidationError("Job seeker data not found.")
            job_seeker_email = job_seeker_data.get('email')
            print(job_seeker_email)
            job_seeker_first_name = job_seeker_data.get('first_name')
            
            # Call the Celery task to send an email
            send_job_offer_notification.delay(
                job_seeker_email,
                job_seeker_first_name,
                job_offer.job_post_id,
                job_offer.amount,
                job_offer.currency
            )
        
        return job_offer


class JobOfferUpdateSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=45, required=False)
    counter_amount = serializers.IntegerField(required=False)
    rejected_reason = serializers.CharField(max_length=1000, required=False, allow_blank=True)

    def validate(self, data):
        if data.get('status') == 'Rejected' and not data.get('rejected_reason'):
            raise serializers.ValidationError("Rejected reason is required when rejecting a job offer.")
        return data
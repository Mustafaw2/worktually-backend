import requests
from rest_framework import serializers
from django.conf import settings
from recruitment.models import JobInterview

class SendInterviewRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobInterview
        fields = [
            'jobpost_id', 'candidate_id', 'interview_method_id', 'start_date', 
            'end_date', 'reschedule_start_date', 'reschedule_end_date', 
            'reschedule_by', 'status', 'feedback', 'meeting_url', 
            'event_id', 'rating', 'expired_at', 'cancel_reason'
        ]

    def validate_candidate_id(self, value):
        # Fetch candidate details
        api_key = settings.API_KEY  # Ensure you have the API key in your settings
        candidate_api_url = f"http://localhost:8001/api/candidates/{value}/"
        headers = {'Authorization': f'Api-Key {api_key}'}
        response = requests.get(candidate_api_url, headers=headers)
        
        if response.status_code != 200:
            raise serializers.ValidationError("Candidate does not exist or could not be retrieved.")
        
        candidate_response = response.json()
        candidate_data = candidate_response.get('data', {})
        
        if not candidate_data:
            raise serializers.ValidationError("Candidate data not found.")

        job_seeker_id = candidate_data.get('job_seeker_id')
        if not job_seeker_id:
            raise serializers.ValidationError("Job seeker ID not found in candidate data.")
        
        # Fetch job seeker details
        job_seeker_api_url = f"http://localhost:8001/api/job_seeker/list/{job_seeker_id}/"
        response = requests.get(job_seeker_api_url, headers=headers)
        
        if response.status_code != 200:
            raise serializers.ValidationError("Job seeker does not exist or could not be retrieved.")
        

        job_seeker_response = response.json()
        
        job_seeker_data = job_seeker_response.get('data', {})
        if not job_seeker_data:
            raise serializers.ValidationError("Job seeker data not found.")
        first_name = job_seeker_data.get('first_name')
        email = job_seeker_data.get('email')

        # Ensure email and first name are present
        if not first_name:
            raise serializers.ValidationError("Job seeker does not have a first name.")
        if not email:
            raise serializers.ValidationError("Job seeker does not have an email.")
        
        # Optionally, you can attach these details to the serializer's context or return them
        self.context['job_seeker_first_name'] = first_name
        self.context['job_seeker_email'] = email

        return value

    def create(self, validated_data):
        # Create the JobInterview instance
        job_interview = JobInterview.objects.create(**validated_data)
        
        # Retrieve job seeker details from the context
        job_seeker_email = self.context.get('job_seeker_email')
        
        if job_seeker_email:
            # Here you would send the email to the job seeker
            # Example: send_interview_email(job_seeker_email)
            pass
        
        return job_interview




class RescheduleInterviewSerializer(serializers.Serializer):
    reschedule_start_date = serializers.DateTimeField()
    reschedule_end_date = serializers.DateTimeField()
    reschedule_by = serializers.CharField(max_length=45)
    cancel_reason = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        if data['reschedule_start_date'] >= data['reschedule_end_date']:
            raise serializers.ValidationError("Reschedule start date must be before end date.")
        return data

class AcceptRejectInterviewSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[("Accepted", "Accepted"), ("Rejected", "Rejected")])
    feedback = serializers.CharField(max_length=255, required=False)
    reschedule_start_date = serializers.DateTimeField(required=False)
    reschedule_end_date = serializers.DateTimeField(required=False)
    reschedule_by = serializers.CharField(max_length=45, required=False)
    cancel_reason = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        if 'status' in data:
            if data['status'] not in ['Accepted', 'Rejected', 'Rescheduled']:
                raise serializers.ValidationError("Invalid status. Must be 'Accepted', 'Rejected', or 'Rescheduled'.")
            if data['status'] == 'Rejected' and 'cancel_reason' not in data:
                raise serializers.ValidationError("cancel_reason is required when rejecting an interview.")

        return data
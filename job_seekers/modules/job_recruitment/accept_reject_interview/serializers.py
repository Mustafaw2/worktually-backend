import os
import requests
from rest_framework import serializers
from django.utils.dateparse import parse_datetime


class AcceptRejectInterviewSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=45)
    cancel_reason = serializers.CharField(
        max_length=1000, required=False, allow_blank=True
    )

    def update_interview_status(self, interview_id, validated_data):
        api_key = os.getenv("API_KEY")
        url = f"https://dev3-api.worktually.com/api/interviews/{interview_id}/accept-reject/"
        headers = {"Authorization": f"Api-Key {api_key}"}
        response = requests.post(url, headers=headers, json=validated_data)
        if response.status_code != 200:
            raise serializers.ValidationError(response.json())
        return response.json()


class RescheduleInterviewSerializer(serializers.Serializer):
    reschedule_start_date = serializers.DateTimeField()
    reschedule_end_date = serializers.DateTimeField()
    reschedule_by = serializers.CharField(max_length=45)
    cancel_reason = serializers.CharField(max_length=100)

    def validate(self, data):
        # Validate that reschedule start date is before end date
        if data["reschedule_start_date"] >= data["reschedule_end_date"]:
            raise serializers.ValidationError(
                "Reschedule start date must be before end date."
            )
        return data

    def to_internal_value(self, data):
        # Convert date fields from string to datetime objects if they are not already datetime objects
        data = super().to_internal_value(data)
        for field in ["reschedule_start_date", "reschedule_end_date"]:
            if isinstance(data[field], str):
                data[field] = parse_datetime(data[field])
        return data

    def reschedule_interview(self, interview_id, validated_data):
        api_key = os.getenv("API_KEY")
        url = (
            f"https://dev3-api.worktually.com/api/interviews/{interview_id}/reschedule/"
        )
        headers = {"Authorization": f"Api-Key {api_key}"}

        # Ensure validated_data is serialized correctly
        serialized_data = {
            "reschedule_start_date": validated_data["reschedule_start_date"].strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "reschedule_end_date": validated_data["reschedule_end_date"].strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "reschedule_by": validated_data["reschedule_by"],
        }

        response = requests.post(url, headers=headers, json=serialized_data)
        print(response)

        if response.status_code != 200:
            # Handle different types of errors based on response status
            try:
                response_data = response.json()
            except ValueError:
                raise serializers.ValidationError("Invalid response from server.")
            raise serializers.ValidationError(response_data)

        return response.json()

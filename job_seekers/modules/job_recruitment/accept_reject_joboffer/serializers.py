import os
import requests
from rest_framework import serializers


class AcceptRejectJobOfferSerializer(serializers.Serializer):
    action = serializers.CharField(max_length=45)
    counter_amount = serializers.IntegerField(required=False, allow_null=True)
    rejected_reason = serializers.CharField(
        max_length=1000, required=False, allow_blank=True, allow_null=True
    )

    def validate_action(self, value):
        if value not in ["Accept", "Reject", "Counter"]:
            raise serializers.ValidationError("Invalid action value.")
        return value

    def validate(self, data):
        if data["action"] == "Reject" and not data.get("rejected_reason"):
            raise serializers.ValidationError(
                "Rejected reason is required when rejecting a job offer."
            )
        if data["action"] == "Counter" and not data.get("counter_amount"):
            raise serializers.ValidationError(
                "Counter amount is required when countering a job offer."
            )
        return data

    def update_job_offer(self, job_offer_id, validated_data):
        api_key = os.getenv("API_KEY")
        url = f"https://dev3-api.worktually.com/api/job-offers/{job_offer_id}/"
        headers = {"Authorization": f"Api-Key {api_key}"}

        # Prepare payload with only provided fields
        payload = {"status": validated_data["action"].capitalize()}

        if "counter_amount" in validated_data:
            payload["counter_amount"] = validated_data["counter_amount"]

        if "rejected_reason" in validated_data:
            payload["rejected_reason"] = validated_data["rejected_reason"]

        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise serializers.ValidationError(response.json())
        return response.json()

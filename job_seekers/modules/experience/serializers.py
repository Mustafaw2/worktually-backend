from rest_framework import serializers
from job_seekers.modules.experience.models import JobProfileExperience
from job_seekers.models import JobProfile

class JobProfileExperienceSerializer(serializers.ModelSerializer):
    job_profile = serializers.PrimaryKeyRelatedField(
        queryset=JobProfile.objects.all(),  # Ensure to import JobProfile
        required=True
    )

    class Meta:
        model = JobProfileExperience
        fields = [
            "id",
            "job_profile",  # Add job_profile here
            "company_name",
            "start_date",
            "end_date",
            "currently_working",
            "description",
            "country",
            "city",
        ]

    def create(self, validated_data):
        # Assign the job_seeker from the request context
        validated_data['job_seeker'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Assign the job_seeker from the request context
        validated_data['job_seeker'] = self.context['request'].user
        return super().update(instance, validated_data)



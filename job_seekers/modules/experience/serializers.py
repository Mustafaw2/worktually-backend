from rest_framework import serializers
from job_seekers.modules.experience.models import JobProfileExperience
from rest_framework import serializers

class JobProfileExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfileExperience
        fields = [
            "company_name",
            "start_date",
            "end_date",
            "currently_working",
            "description",
            "country",
            "city",
        ]

    def create(self, validated_data):
        validated_data['job_seeker'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['job_seeker'] = self.context['request'].user
        return super().update(instance, validated_data)


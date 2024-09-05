from rest_framework import serializers
from job_seekers.modules.experience.models import JobProfileExperience

class JobProfileExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfileExperience
        fields = [
            "job_seeker",
            "company_name",
            "start_date",
            "end_date",
            "currently_working",
            "description",
            "country",
            "city",
        ]


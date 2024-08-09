from rest_framework import serializers
from job_seekers.modules.experience.models import JobProfileExperience


class JobProfileExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfileExperience
        fields = [
            "job_seeker",
            "title",
            "job_type_id",
            "company_name",
            "start_date",
            "end_date",
            "currently_working",
        ]

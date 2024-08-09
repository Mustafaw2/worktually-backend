from rest_framework import serializers
from job_seekers.modules.job_profiles.models import JobProfile, JobProfilePortfolio


class JobProfileSerializer(serializers.ModelSerializer):
    # job_profile_skills = JobProfileSkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobProfile
        fields = [
            "job_seeker",
            "job_title",
            "ssn_cnic_passport",
            "state",
            "city",
            "address",
        ]
        read_only_fields = ["status"]


class JobProfilePortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfilePortfolio
        fields = "__all__"

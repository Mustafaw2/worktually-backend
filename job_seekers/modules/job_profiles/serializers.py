from rest_framework import serializers
from job_seekers.modules.job_profiles.models import JobProfile, JobProfilePortfolio


class JobProfileSerializer(serializers.ModelSerializer):
    # job_profile_skills = JobProfileSkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobProfile
        fields = fields = [
            "job_profile_name",
            "job_seeker",
            "job_title",
            "hourly_rate"
        ]
        read_only_fields = ["status"]


class JobProfileInfoSerializer(serializers.ModelSerializer):
    # job_profile_skills = JobProfileSkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobProfile
        fields = fields = "__all__"
        read_only_fields = ["status"]


class JobProfilePortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfilePortfolio
        fields = "__all__"

from rest_framework import serializers
from .models import Education


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        ref_name = "JobSeekerEducationSerializer"
        fields = [
            "id",
            "job_seeker",
            "title",
            "education_type_id",
            "major_subjects",
            "institute_name",
        ]

from rest_framework import serializers
from .models import Education

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        ref_name = "JobSeekerEducationSerializer"
        fields = [
            "id",
            "job_seeker",
            "degree_type",
            "discipline",
            "institute_name",
            "from_date",
            "to_date",
        ]
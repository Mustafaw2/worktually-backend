from rest_framework import serializers
from .models import JobSeeker


class BasicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeeker
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "gender",
            "country",
        ]

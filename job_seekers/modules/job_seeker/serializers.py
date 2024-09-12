from rest_framework import serializers
from .models import JobSeeker
from lookups.modules.cities.serializers import CitySerializer
from lookups.modules.countries.serializers import CountrySerializer
from lookups.modules.states.serializers import StateSerializer

class BasicProfileSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)
    state = StateSerializer(read_only=True)

    class Meta:
        model = JobSeeker
        fields = [
            "profile_picture",
            "first_name",
            "last_name",
            "email",
            "phone",
            "birth_date",
            "gender",
            "id_number",        
            "timezone",
            "country",
            "city",
            "state",
        ]


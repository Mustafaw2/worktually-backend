from rest_framework import serializers
from .models import Language
from lookups.serializers import LanguagesSerializer

class LanguageSerializer(serializers.ModelSerializer):
    language = LanguagesSerializer()
    class Meta:
        model = Language
        fields = ['id', 'job_seeker', 'language', 'proficiency', 'created_at', 'updated_at']
        read_only_fields = ['job_seeker', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set the job_seeker to the logged-in user from the request context
        job_seeker = self.context['request'].user
        validated_data['job_seeker'] = job_seeker
        return super().create(validated_data)



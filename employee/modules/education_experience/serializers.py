from rest_framework import serializers
from .models import Education, Experience

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

    # def validate(self, data):
    #     if 'score' in data:
    #         score = int(data['score'])  
    #         if not (0 <= score <= 100):
    #             raise serializers.ValidationError("Score must be between 0 and 100.")
    #     return data



class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
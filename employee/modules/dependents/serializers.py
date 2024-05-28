from rest_framework import serializers
from .models import Dependent

class DependentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependent
        fields = ['id', 'name', 'relation', 'id_number', 'social_insurance_number']

    def create(self, validated_data):
        user = validated_data.get('user')
        if not user:
            raise serializers.ValidationError("User does not exist.")
        return super().create(validated_data)
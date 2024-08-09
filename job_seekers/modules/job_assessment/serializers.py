from rest_framework import serializers
from .models import JobTitle, JobTitleAssessment


class JobTitleAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobTitleAssessment
        fields = ["id", "question", "options"]


class GetAssessmentQuestionsSerializer(serializers.Serializer):
    job_title_id = serializers.IntegerField()


class SubmissionSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option = serializers.CharField(max_length=255)


class AssessmentResultRequestSerializer(serializers.Serializer):
    job_profile_id = serializers.IntegerField()
    job_title_id = serializers.IntegerField()
    submission = serializers.ListField(child=SubmissionSerializer())


class AssessmentResultResponseSerializer(serializers.Serializer):
    employee_job_profile_id = serializers.IntegerField()
    obtained_marks = serializers.IntegerField()
    total_marks = serializers.IntegerField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    message = serializers.CharField()


class TestResultSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer = serializers.CharField()


class GetResultsResponseSerializer(serializers.Serializer):
    job_profile_id = serializers.IntegerField()
    test_result = serializers.ListField(child=TestResultSerializer())
    obtained_marks = serializers.IntegerField()
    total_marks = serializers.IntegerField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    message = serializers.CharField()

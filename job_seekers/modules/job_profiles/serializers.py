from rest_framework import serializers
from job_seekers.modules.job_profiles.models import JobProfile, JobProfilePortfolio
from job_seekers.modules.education.serializers import EducationSerializer
from job_seekers.modules.experience.serializers import JobProfileExperienceSerializer
from job_seekers.modules.languages.serializers import LanguageSerializer
from job_seekers.modules.job_assessment.serializers import GetResultsResponseSerializer
from job_seekers.modules.skills.serializers import JobProfileSkillSerializer
from job_seekers.models import JobProfileSkill


class JobProfileSerializer(serializers.ModelSerializer):
    # job_profile_skills = JobProfileSkillSerializer(many=True, read_only=True)

    class Meta:
        model = JobProfile
        fields = fields = [
            "job_seeker",
            "job_title",
            "hourly_rate"
        ]
        read_only_fields = ["status"]





class JobProfilePortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProfilePortfolio
        fields = [
            'id', 'job_profile', 'project_title', 'description', 'url',  'created_at', 'updated_at'
        ]


class JobProfileInfoSerializer(serializers.ModelSerializer):
    education = EducationSerializer(many=True, read_only=True, source='job_seeker.Education')
    experience = JobProfileExperienceSerializer(many=True, read_only=True, source='job_seeker.jobprofile_experiences')
    skills = JobProfileSkillSerializer(many=True, read_only=True, source='job_profile_skills')
    assessment = GetResultsResponseSerializer(many=True, source='assessments')
    languages = LanguageSerializer(many=True, source='job_seeker.language')

    class Meta:
        model = JobProfile
        fields = [
            'id', 'status', 'job_seeker', 'job_title',
            'hourly_rate', 'completion_rate', 'priority', 'reviewed_at',
            'rating', 'is_approved', 'education', 'experience', 'skills',
            'assessment', 'languages'
        ]

        def get_skills(self, obj):
            job_profile_skills = JobProfileSkill.objects.filter(job_profile=obj)
            categorized_skills = {}
            
            for job_profile_skill in job_profile_skills:
                skill = job_profile_skill.skill
                category_name = skill.skill_category.name  # Get the skill category name
                
                if category_name not in categorized_skills:
                    categorized_skills[category_name] = []
                
                categorized_skills[category_name].append(JobProfileSkillSerializer(skill).data)
            
            return categorized_skills

from rest_framework import serializers
from lookups.models import SkillCategory, SoftSkills, AdminSoftware, ProgrammingLanguage, AccountingSkills, Database, Frameworks, CommunicationSkills, CMS

class SoftSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftSkills
        fields = ['id', 'name']

class AdminSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminSoftware
        fields = ['id', 'name']

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgrammingLanguage
        fields = ['id', 'name']

class AccountingSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountingSkills
        fields = ['id', 'name']

class DatabasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = ['id', 'name']

class FrameworksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frameworks
        fields = ['id', 'name']

class CommunicationSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunicationSkills
        fields = ['id', 'name']


class CmsSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CMS
        fields = ['id', 'name']      


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'skills']

    def get_skills(self, obj):
        skill_map = {
            'soft_skills': SoftSkillsSerializer,
            'admin_software': AdminSoftwareSerializer,
            'programming_languages': ProgrammingLanguageSerializer,
            'accounting_skills': AccountingSkillsSerializer,
            'databases': DatabasesSerializer,
            'cms' : CmsSkillsSerializer,
            'frameworks': FrameworksSerializer,
            'communication_skills': CommunicationSkillsSerializer,
        }

        for skill_type, serializer_class in skill_map.items():
            skills = getattr(obj, skill_type).all()
            if skills.exists():
                return serializer_class(skills, many=True).data
        
        return []

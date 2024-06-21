from django.db import models

class SkillCategory(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class Skill(models.Model):
    skill_category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name

class JobProfileSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='job_profile_skills')
    job_profile_id = models.IntegerField()

    def __str__(self):
        return f"{self.skill.name} for profile {self.job_profile_id}"

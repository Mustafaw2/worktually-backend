# from django.db import models
# from job_seekers.models import JobSeeker

# class Language(models.Model):
#     job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='languages')
#     language_id = models.CharField(max_length=45)
#     level = models.CharField(max_length=45)

#     def __str__(self):
#         return self.language_id

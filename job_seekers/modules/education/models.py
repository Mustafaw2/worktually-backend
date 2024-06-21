# from django.db import models
# from job_seekers.models import JobSeeker

# class Education(models.Model):
#     job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='educations')
#     title = models.CharField(max_length=45)
#     education_type_id = models.CharField(max_length=45)
#     major_subjects = models.CharField(max_length=45)
#     score = models.CharField(max_length=45)
#     completion_date = models.DateField()
#     institute_name = models.CharField(max_length=45)
#     certificate_photo = models.CharField(max_length=45)

#     def __str__(self):
#         return self.title

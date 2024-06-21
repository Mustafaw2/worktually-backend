from django.db import models

class JobProfile(models.Model):
    job_seeker = models.ForeignKey('job_seekers.JobSeeker', on_delete=models.CASCADE, related_name='job_profile')
    job_title_id = models.CharField(max_length=45)
    hourly_rate = models.CharField(max_length=45)
    currency = models.CharField(max_length=45)
    completion_rate = models.IntegerField()
    disabled = models.BooleanField()
    priority = models.IntegerField()
    status = models.CharField(max_length=45)
    reviewed_at = models.CharField(max_length=45)
    rating = models.CharField(max_length=45)

    def __str__(self):
        return self.job_title_id

class JobProfileReview(models.Model):
    job_profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE, related_name='reviews')
    communication_rating = models.FloatField()
    experience_rating = models.FloatField()
    education_rating = models.FloatField()
    skills_rating = models.FloatField()
    comments = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    reject_reason_id = models.IntegerField()
    next_review = models.DateField()
    reviewed_by = models.IntegerField()

    def __str__(self):
        return self.comments

class JobProfilePortfolio(models.Model):
    job_profile = models.ForeignKey(JobProfile, on_delete=models.CASCADE, related_name='portfolios')
    title = models.CharField(max_length=45)
    description = models.TextField()
    tags = models.TextField()
    url = models.CharField(max_length=45)
    files = models.TextField()

    def __str__(self):
        return self.title

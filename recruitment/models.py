from django.db import models
from recruitment.modules.API_keys.models import APIKey
import requests
import os
class JobPost(models.Model):
    organization_id = models.IntegerField(null=True, blank=True)
    manager_id = models.IntegerField()
    job_title_id = models.IntegerField()
    job_type_id = models.IntegerField()
    description = models.TextField()
    slug = models.TextField()
    salary_type_id = models.IntegerField()
    amount = models.IntegerField()
    experience_required = models.IntegerField()
    education_required = models.TextField()
    skills = models.TextField()
    gender = models.CharField(max_length=45)
    status = models.CharField(max_length=45)
    closed_reason = models.TextField()
    expired_date = models.DateTimeField()
    shift_type_id = models.IntegerField()
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    shift_hours = models.IntegerField()

    def __str__(self):
        return f"JobPost {self.id}: {self.description[:50]}..."
    

class JobInterview(models.Model):
    jobpost_id = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    candidate_id = models.CharField(max_length=45)
    interview_method_id = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reschedule_start_date = models.DateTimeField(null=True, blank=True)
    reschedule_end_date = models.DateTimeField(null=True, blank=True)
    reschedule_by = models.CharField(max_length=45, null=True, blank=True)
    status = models.CharField(max_length=45)
    feedback = models.TextField()
    meeting_url = models.TextField()
    event_id = models.TextField()
    rating = models.TextField()
    expired_at = models.CharField(max_length=45)
    cancel_reason = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"JobInterview {self.id} for JobPost {self.job_post_id}"

class JobOffer(models.Model):
    job_post_id = models.IntegerField()
    candidate_id = models.CharField(max_length=45)
    currency = models.CharField(max_length=45)
    amount = models.IntegerField()
    counter_amount = models.IntegerField()
    counter_by = models.TextField()
    status = models.CharField(max_length=45)
    rejected_reason = models.TextField()
    expired_at = models.CharField(max_length=45)

    def __str__(self):
        return f"JobOffer {self.id} for JobPost {self.job_post_id}"
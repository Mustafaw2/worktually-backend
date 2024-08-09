from django.db import models


class Language(models.Model):
    job_seeker = models.ForeignKey(
        "job_seekers.JobSeeker", on_delete=models.CASCADE, related_name="language"
    )
    language_id = models.CharField(max_length=45)
    level = models.CharField(max_length=45)

    class Meta:
        app_label = 'job_seekers'

    def __str__(self):
        return self.language_id

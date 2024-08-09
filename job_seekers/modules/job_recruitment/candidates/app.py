from django.apps import AppConfig


class JobSeekersConfig(AppConfig):
    name = "job_seekers.modules.job_recruitment.candidates"

    def ready(self):
        import job_seekers.modules.job_recruitment.candidates.signals

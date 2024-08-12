import os
import json
from django.core.management.base import BaseCommand
from job_seekers.models import JobTitle


class Command(BaseCommand):
    help = "Populates the JobTitle model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "jobtitles.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the JobTitle model
        for item in data:
            JobTitle.objects.get_or_create(name=item["name"])

        self.stdout.write(self.style.SUCCESS("Successfully populated JobTitle model."))
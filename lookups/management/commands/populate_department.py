import os
import json
from django.core.management.base import BaseCommand
from lookups.models import Department

class Command(BaseCommand):
    help = "Populates the Department model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "department.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the Department model
        for item in data:
            Department.objects.get_or_create(name=item["name"], defaults={"status": item["status"]})

        self.stdout.write(self.style.SUCCESS("Successfully populated Department model."))

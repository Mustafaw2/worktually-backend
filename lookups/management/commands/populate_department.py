import os
import json
from django.core.management.base import BaseCommand
from lookups.models import Source


class Command(BaseCommand):
    help = "Populates the Source model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "source.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the Source model
        for item in data:
            source, created = Source.objects.get_or_create(
                name=item["name"],
                defaults={"status": item["status"]}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added {source.name} to Source table."))
            else:
                self.stdout.write(f"{source.name} already exists.")

        self.stdout.write(self.style.SUCCESS("Successfully populated Source model."))

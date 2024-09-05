import os
import json
from django.core.management.base import BaseCommand
from lookups.models import DegreeTitle, DegreeType

class Command(BaseCommand):
    help = "Populates the Degree model with data from a JSON file"

    def handle(self, *args, **kwargs):
        # Construct the file path
        file_path = os.path.join("lookups", "fixtures", "degree_titles.json")

        # Open and read the JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Populate the Degree model
        for item in data:
            # Fetch the DegreeType instance
            degree_type = DegreeType.objects.get(id=item["degree_type_id"])

            # Create or get the Degree instance
            DegreeTitle.objects.get_or_create(
                name=item["name"],
                active_status=item["active_status"] == 1,  # Convert 1 to True and 0 to False
                degree_type=degree_type
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated Degree model."))


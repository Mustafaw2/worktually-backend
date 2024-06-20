import os
import json
from django.core.management.base import BaseCommand
from lookups.models import Industry


class Command(BaseCommand):
    help = 'Populate Industry model from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('lookups','fixtures', 'industries.json')  # Adjust the path to your JSON file
        
        with open(file_path, 'r') as file:
            industries = json.load(file)
            
            for industry_data in industries:
                name = industry_data.get('name')
                
                if name:
                    # Create or update Industry object based on 'name'
                    industry, created = Industry.objects.update_or_create(
                        name=name,
                        defaults={'status': 'Active'}  # Assuming 'Active' status for new entries
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Industry '{name}' added successfully"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Industry '{name}' already exists"))
                else:
                    self.stdout.write(self.style.ERROR("Invalid industry data: 'name' field is missing"))
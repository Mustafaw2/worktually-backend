import os
import json
from django.core.management.base import BaseCommand
from lookups.models import Skill


class Command(BaseCommand):
    help = 'Populate Industry model from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('lookups','fixtures', 'skill_categories.json')  
        
        with open(file_path, 'r') as file:
            degree_subjects = json.load(file)
            
            for subject_data in degree_subjects:
                name = subject_data.get('name')
                
                if name:
                    # Create or update DegreeSubject object based on 'name'
                    subject, created = Skill.objects.update_or_create(
                        name=name,
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Degree subject '{name}' added successfully"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"Degree subject '{name}' already exists"))
                else:
                    self.stdout.write(self.style.ERROR("Invalid degree subject data: 'name' field is required"))
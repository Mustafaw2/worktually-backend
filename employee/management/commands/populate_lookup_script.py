import os
import json
from django.core.management.base import BaseCommand
from employee.models import Lookup

class Command(BaseCommand):
    help = 'Populate Lookup table with countries from countries.json'
    def handle(self, *args, **kwargs):
        filepath = os.path.join('employee', 'fixtures', 'degree_subjects.json')  # Path to your degree_subjects.json file
        with open(filepath, 'r') as file:
            degree_subjects_data = json.load(file)
            for degree_subject_data in degree_subjects_data:
                degree_subject_name = degree_subject_data['name']
                # Check if the degree subject already exists in the table
                if not Lookup.objects.filter(category='Degree Subject', name=degree_subject_name).exists():
                    degree_subject = Lookup.objects.create(
                        category='Degree Subject',
                        name=degree_subject_name,
                    )
                    degree_subject.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated Lookup table with degree subjects'))
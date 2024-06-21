import os
import json
from django.core.management.base import BaseCommand
from lookups.models import State, Country


class Command(BaseCommand):
    help = 'Populate State model from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('lookups', 'fixtures', 'states.json')
        
        with open(file_path, 'r', encoding='utf-8') as file:
            states_data = json.load(file)
            
            for state_data in states_data:
                state_id = state_data.get('id')
                name = state_data.get('name')
                country_id = state_data.get('country_id')
                state_code = state_data.get('state_code')

                if state_id and name and country_id and state_code:
                    try:
                        country = Country.objects.get(id=country_id)
                        state, created = State.objects.update_or_create(
                            id=state_id,
                            defaults={
                                'name': name,
                                'country': country,
                                'state_code': state_code
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"State '{name}' added successfully"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"State '{name}' updated successfully"))
                    except Country.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Country with id '{country_id}' does not exist"))
                else:
                    self.stdout.write(self.style.ERROR("Invalid state data: 'id', 'name', 'country_id', and 'state_code' fields are required"))

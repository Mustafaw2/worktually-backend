import os
import json
from django.core.management.base import BaseCommand
from lookups.models import City, State, Country


class Command(BaseCommand):
    help = 'Populate City model from JSON file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join('lookups', 'fixtures', 'file-2.json')
        
        with open(file_path, 'r', encoding='utf-8') as file:
            cities_data = json.load(file)
            
            for city_data in cities_data:
                city_id = city_data.get('id')
                name = city_data.get('name')
                state_id = city_data.get('state_id')
                country_id = city_data.get('country_id')
                country_code = city_data.get('country_code')
                latitude = city_data.get('latitude')
                longitude = city_data.get('longitude')

                if city_id and name and state_id and country_id and country_code and latitude and longitude:
                    try:
                        state = State.objects.get(id=state_id)
                        city, created = City.objects.update_or_create(
                            id=city_id,
                            defaults={
                                'name': name,
                                'state': state,
                                'country_id': country_id,
                                'country_code': country_code,
                                'latitude': latitude,
                                'longitude': longitude
                            }
                        )
                        if created:
                            self.stdout.write(self.style.SUCCESS(f"City '{name}' added successfully"))
                        else:
                            self.stdout.write(self.style.SUCCESS(f"City '{name}' updated successfully"))
                    except State.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"State with id '{state_id}' does not exist"))
                else:
                    self.stdout.write(self.style.ERROR("Invalid city data: 'id', 'name', 'state_id', 'country_id', 'country_code', 'latitude', and 'longitude' fields are required"))

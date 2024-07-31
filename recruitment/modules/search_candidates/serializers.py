import os
import requests
from rest_framework import serializers
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

class CandidateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()

    @staticmethod
    def fetch_candidate(candidate_id):
        api_key = os.getenv("API_KEY")
        headers = {"Authorization": f"Api-Key {api_key}"}
        url = f"https://seekerdev3-api.worktually.com/api/candidates/{candidate_id}/"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json(), None
        elif response.status_code == 404:
            return None, "Candidate not found"
        else:
            return None, "An error occurred while retrieving the candidate"

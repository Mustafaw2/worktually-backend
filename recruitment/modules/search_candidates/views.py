from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import CandidateSerializer

class CandidateSearchView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Search candidate by candidate ID",
        responses={
            200: openapi.Response(
                description="Success",
                examples={
                    "application/json": {
                        "success": True,
                        "message": "Candidate retrieved successfully",
                        "data": {
                            "id": 1,
                            "name": "Candidate 1",
                            "email": "candidate1@example.com"
                        },
                    }
                },
            ),
            404: openapi.Response(description="Candidate not found"),
            500: openapi.Response(description="API key not found or server error"),
        },
    )
    def get(self, request, pk):
        data, error = CandidateSerializer.fetch_candidate(pk)
        if error:
            return JsonResponse({
                "success": False,
                "message": error
            }, status=404 if error == "Candidate not found" else 500)

        return JsonResponse({
            "success": True,
            "message": "Candidate retrieved successfully",
            "data": data
        }, status=200)

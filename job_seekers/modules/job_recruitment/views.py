from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
from rest_framework.permissions import IsAuthenticated


class JobPostListView(APIView):

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get a list of job posts by organization",
        manual_parameters=[
            openapi.Parameter(
                "organization_id",
                openapi.IN_QUERY,
                description="ID of the organization",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: "Success", 400: "Bad Request"},
    )
    def get(self, request, *args, **kwargs):
        organization_id = request.query_params.get("organization_id")
        if not organization_id:
            return Response(
                {"message": "organization_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Assuming the recruitment API is hosted locally on port 8000
            response = requests.get(
                f"https://dev3-api.worktually.com/api/recruitment/job-posts/{organization_id}/"
            )
            response_data = response.json()

            if response.status_code == 200:
                return Response(
                    {"message": "Success", "data": response_data},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "message": "Failed to retrieve job posts from recruitment API",
                        "details": response_data,
                    },
                    status=response.status_code,
                )
        except requests.exceptions.RequestException as e:
            return Response(
                {"message": "Error connecting to recruitment API", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

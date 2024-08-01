from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from recruitment.models import JobOffer
from .serializers import JobOfferSerializer

class SendJobOfferView(APIView):
    @swagger_auto_schema(
        request_body=JobOfferSerializer,
        responses={
            201: openapi.Response("Created", JobOfferSerializer),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = JobOfferSerializer(data=request.data)
        if serializer.is_valid():
            job_offer = serializer.save()
            return Response({
                "message": "Job offer sent successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "errors": serializer.errors,
            "message": "There were validation errors."
        }, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import SendInterviewRequestSerializer
from recruitment.tasks import send_interview_notification
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from recruitment.models import JobInterview
from .serializers import *

class SendInterviewRequestView(APIView):
    def post(self, request):
        serializer = SendInterviewRequestSerializer(data=request.data)
        if serializer.is_valid():
            job_interview = serializer.save()
            
            # Retrieve job seeker details from serializer context
            job_seeker_email = serializer.context.get('job_seeker_email')
            job_seeker_first_name = serializer.context.get('job_seeker_first_name')

            # Extract necessary fields from job_interview
            job_post_id = job_interview.jobpost_id.id
            interview_method_id = job_interview.interview_method_id
            start_date = job_interview.start_date
            end_date = job_interview.end_date
            
            # Call the Celery task to send an email
            send_interview_notification.delay(
                job_seeker_email,
                job_seeker_first_name,
                job_post_id,
                interview_method_id,
                start_date,
                end_date
            )
            
            return Response({"message": "Interview request sent successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





class RescheduleInterviewView(APIView):

    def post(self, request, pk):
        try:
            job_interview = JobInterview.objects.get(pk=pk)
        except JobInterview.DoesNotExist:
            return Response({"error": "Job interview not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = RescheduleInterviewSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            job_interview.reschedule_start_date = data['reschedule_start_date']
            job_interview.reschedule_end_date = data['reschedule_end_date']
            job_interview.reschedule_by = data['reschedule_by']
            job_interview.cancel_reason = data['cancel_reason']
            job_interview.status = "Rescheduled"
            job_interview.save()

            return Response({"message": "Success", "data": SendInterviewRequestSerializer(job_interview).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptRejectInterviewView(APIView):

    def post(self, request, pk):
        try:
            job_interview = JobInterview.objects.get(pk=pk)
        except JobInterview.DoesNotExist:
            return Response({"error": "Job interview not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = AcceptRejectInterviewSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            job_interview.status = data['status']
            if data['status'] == "Rejected":
                job_interview.cancel_reason = data.get('cancel_reason', '')
            elif data['status'] == "Accepted":
                job_interview.reschedule_start_date = None
                job_interview.reschedule_end_date = None
                job_interview.reschedule_by = None
                job_interview.cancel_reason = None

            job_interview.save()

            return Response({"message": "Success", "data": SendInterviewRequestSerializer(job_interview).data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
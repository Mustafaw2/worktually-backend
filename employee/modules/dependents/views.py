from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Dependent
from .serializers import DependentSerializer

class DependentsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        dependents = Dependent.objects.filter(user=request.user)
        serializer = DependentSerializer(dependents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddDependentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DependentSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response({'message': 'Dependent added successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditDependentView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, dependent_id):
        try:
            dependent = Dependent.objects.get(id=dependent_id, user=request.user)
        except Dependent.DoesNotExist:
            return Response({"error": "Dependent not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DependentSerializer(dependent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Dependent updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, dependent_id):
        try:
            dependent = Dependent.objects.get(id=dependent_id, user=request.user)
        except Dependent.DoesNotExist:
            return Response({"error": "Dependent not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DependentSerializer(dependent, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Dependent updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteDependentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, dependent_id):
        try:
            dependent = Dependent.objects.get(id=dependent_id, user=request.user)
        except Dependent.DoesNotExist:
            return Response({"error": "Dependent not found."}, status=status.HTTP_404_NOT_FOUND)

        dependent.delete()
        return Response({"message": "Dependent deleted successfully."}, status=status.HTTP_200_OK)
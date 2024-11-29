from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.backend.serializers import ErrorSerializer

class ErrorDetailView(APIView):
    def get(self, request, *args, **kwargs):
        error = {"name": "error_1", "timestamp_start": 1.0, "timestamp_end": 3.0}
        serializer = ErrorSerializer(error)
        return Response(serializer.data, status=status.HTTP_200_OK)

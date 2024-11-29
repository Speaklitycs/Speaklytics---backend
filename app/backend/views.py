from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from app.backend.serializers import ErrorSerializer, VideoUploadSerializer

class ErrorDetailView(APIView):
    def get(self, request, *args, **kwargs):
        error = {"name": "error_1", "timestamp_start": 1.0, "timestamp_end": 3.0}
        serializer = ErrorSerializer(error)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VideoUploadView(APIView):
    parser_class = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        serializer = VideoUploadSerializer(data=request.data)
        if serializer.is_valid():
            video_file = serializer.validated_data['video']
            with open(f"videos/{video_file.name}.mp4", "wb+") as f:
                for chunk in video_file.chunks():
                    f.write(chunk)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse
from moviepy.video.io.VideoFileClip import VideoFileClip
from app.backend.models import ErrorModel
from app.backend.serializers import ErrorSerializer


class NewTicketView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            error = ErrorModel.objects.create()
        except IntegrityError as e:
            return Response(
                {"message": "Database integrity error while creating the ticket.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as e:
            return Response(
                {"message": "Validation error occurred.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DatabaseError as e:
            return Response(
                {"message": "Database error occurred while creating the ticket.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return Response(
                {"message": "An unexpected error occurred.", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response = {"ticket_id": error.id}
        return Response(response, status=status.HTTP_200_OK)



class ErrorDetailView(APIView):
    def get(self, request, *args, **kwargs):
        error = {"name": "error_1", "timestamp_start": 1.0, "timestamp_end": 3.0}
        serializer = ErrorSerializer(error)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class VideoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser] 
    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('file')
        ticket_id = request.data.get('ticket_id')

        if not video_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if ticket_id is None:
            return Response({"error": "No ticket ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        if ErrorModel.objects.filter(id=ticket_id).exists() is False:
            return Response({"error": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if video_file.content_type != "video/mp4":
            return Response({"error": "Invalid file format"}, status=status.HTTP_400_BAD_REQUEST)

        if video_file.size > 1 * 1024 * 1024 * 1024:
            return Response({"error": "File is too large"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with open(f"video/{ticket_id}.mp4", "wb+") as f:
                for chunk in video_file.chunks():
                    f.write(chunk)
        except FileNotFoundError:
            return Response({"error": "Failed to save the file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "File uploaded successfully"}, status=status.HTTP_201_CREATED)
    

class VideoStreamView(APIView):
    def get(self, request, *args, **kwargs):
        ticket_id = request.data.get('ticket_id')
        time = float(request.data.get('time')) 

        try:
            video_path = f"video/{ticket_id}.mp4"
            with VideoFileClip(video_path) as clip:
                start_time = time
                end_time = min(start_time + 10, clip.duration)

                subclip = clip.subclip(start_time, end_time)

            def stream_video():
                    yield from subclip.iter_frames(fps=30)

            response = StreamingHttpResponse(stream_video(), content_type="video/mp4")
            response['Content-Disposition'] = f'attachment; filename="{ticket_id}_{start_time}_{end_time}.mp4"'
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class TicketAnalyzeView(APIView):
    def post(self, request, *args, **kwargs):
        ticket_id = request.data.get('ticket_id')
        if ticket_id is None or ticket_id not in ErrorModel.objects.values_list('id', flat=True):
            return Response({"error": "No or not existing ticket ID provided"}, status=status.HTTP_400_BAD_REQUEST)
        analysis_type = request.data.get('type')
        if analysis_type is None:
            return Response({"error": "No analysis type provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        

        


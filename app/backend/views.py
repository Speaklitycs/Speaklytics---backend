import os
import threading
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from django.http import StreamingHttpResponse
from app.backend.models import ErrorModel, TicketModel
from app.backend.serializers import ErrorSerializer
from analysis.analysis_base_class import AnalysisBaseClass
from analysis.analysis_mapper import AnalysisMapper, WrongAnalysisTypeException
from speech2text import speech2text
from tempfile import NamedTemporaryFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from rest_framework.decorators import api_view
from moviepy.video.io.VideoFileClip import VideoFileClip



class NewTicketView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            ticket = TicketModel.objects.create()
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

        response = {"ticket-id": ticket.ticket_id}
        return Response(response, status=status.HTTP_200_OK)



class ErrorDetailView(APIView):
    def get(self, request, *args, **kwargs):
        error = {"name": "error_1", "timestamp_start": 1.0, "timestamp_end": 3.0}
        serializer = ErrorSerializer(error)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class VideoUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser] 
    def post(self, request, *args, **kwargs):
        video_file = request.body
        ticket_id = request.query_params.get('ticket-id')

        if not video_file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        if ticket_id is None:
            return Response({"error": "No ticket ID provided"}, status=status.HTTP_400_BAD_REQUEST)

        if TicketModel.objects.filter(ticket_id=ticket_id).exists() is False:
            return Response({"error": "Ticket does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if request.content_type != "application/octet-stream":
            return Response({"error": "Invalid file format"}, status=status.HTTP_400_BAD_REQUEST)

        if len(video_file) > 1 * 1024 * 1024 * 1024:
            return Response({"error": "File is too large"}, status=status.HTTP_400_BAD_REQUEST)
        

        
        try:
            with open(f"data/videos/{ticket_id}.mp4", "wb+") as f:
                f.write(video_file)  # Write the entire bytes object directly
        except FileNotFoundError:
            return Response({"error": "Failed to save the file"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            speech2text.Speech2Text(f"data/videos/{ticket_id}.mp4", f"data/audios/{ticket_id}.wav", 
                        f"data/transcripts/{ticket_id}.json").extract_transcript_and_audio()
        except:
            return Response({"error": "Failed to extract audio or transcript"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"message": "File uploaded successfully"}, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        try:
            ticket_id = int(request.query_params.get('ticket-id'))
        except ValueError:
            return Response({"error": "Invalid ticket ID provided"}, status=400)

        if ticket_id not in TicketModel.objects.values_list('ticket_id', flat=True):
            return Response({"error": "No or not existing ticket ID provided"}, status=400)


        video_path = f"data/videos/{ticket_id}.mp4"
        if not os.path.isfile(video_path):
            return Response({"status": "not-uploaded"}, status=404)
        with VideoFileClip(video_path) as clip:
            def file_iterator(filename, chunk_size=8192):
                with open(filename, "rb") as f:
                    while True:
                        data = f.read(chunk_size)
                        if not data:
                            break
                        yield data

            def cleanup_temp_file(_):
                try:
                    os.remove(output_path)
                except OSError:
                    pass

            try:

                with NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
                    output_path = tmp_file.name
                clip.write_videofile(
                    output_path,
                    codec="libx264", 
                    audio_codec="aac", 
                    fps=24,    
                    temp_audiofile="temp-audio.m4a",
                    remove_temp=True,   
                    logger=None   
                )
                response = StreamingHttpResponse(
                    file_iterator(output_path),
                    content_type="application/octet-stream"
                )
                response["Content-Disposition"] = (
                    f'attachment; filename="{ticket_id}.mp4"'
                )
                response.close = lambda close_original=response.close: (
                    close_original(), cleanup_temp_file(None)
                )

                return response
            
            except Exception as e:
                    return Response({"error": str(e)}, status=500)
    

class VideoStreamView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            ticket_id = int(request.query_params.get('ticket-id'))
        except ValueError:
            return Response({"error": "Invalid ticket ID provided"}, status=400)
        
        try:
            start_time = float(request.query_params.get('time')) 
        except ValueError:
            return Response({"error": "Invalid time provided"}, status=400)

        if ticket_id not in TicketModel.objects.values_list('ticket_id', flat=True):
            return Response({"error": "No or not existing ticket ID provided"}, status=400)


        video_path = f"video/{ticket_id}.mp4"
        if not os.path.isfile(video_path):
            return Response({"status": "not-uploaded"}, status=404)
        with VideoFileClip(video_path) as clip:
            def file_iterator(filename, chunk_size=8192):
                with open(filename, "rb") as f:
                    while True:
                        data = f.read(chunk_size)
                        if not data:
                            break
                        yield data

            def cleanup_temp_file(_):
                try:
                    os.remove(output_path)
                except OSError:
                    pass

            try:
                end_time = min(start_time + 5, clip.duration)
                subclip = clip.subclip(start_time, end_time)

                with NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
                    output_path = tmp_file.name
                subclip.write_videofile(
                    output_path,
                    codec="libx264", 
                    audio_codec="aac", 
                    fps=24,    
                    temp_audiofile="temp-audio.m4a",
                    remove_temp=True,   
                    logger=None   
                )
                response = StreamingHttpResponse(
                    file_iterator(output_path),
                    content_type="video/mp4"
                )
                response["Content-Disposition"] = (
                    f'attachment; filename="{ticket_id}_{int(start_time)}_{int(end_time)}.mp4"'
                )
                response.close = lambda close_original=response.close: (
                    close_original(), cleanup_temp_file(None)
                )

                return response
            
            except Exception as e:
                    return Response({"error": str(e)}, status=500)
            
        
class TicketAnalyzeView(APIView):
    def post(self, request, *args, **kwargs):
        ticket_id = int(request.query_params.get('ticket-id'))
        analysis_type = request.query_params.get('type')
        transcript_path = f"data/transcripts/{ticket_id}.json"
                
        if ticket_id is None or ticket_id not in TicketModel.objects.values_list('ticket_id', flat=True):
            return Response({"error": "No or not existing ticket ID provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if analysis_type is None:
            return Response({"error": "No analysis type provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not os.path.isfile(transcript_path):
            return Response({"error": "Transcript file does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        if analysis_type == "transcription":
             return Response({"status": "success"}, status=status.HTTP_200_OK)
        
        try:
            analysis_class: AnalysisBaseClass = AnalysisMapper().get_analysis_class(analysis_type)
        except WrongAnalysisTypeException:
            return Response({"error": f"Wrong analysis type: {analysis_type}"}, status=status.HTTP_400_BAD_REQUEST)
        
        threading.Thread(target=ErrorModel.analyze, args=(analysis_type, transcript_path, ticket_id)).start()
        return Response({"status": "success"}, status=status.HTTP_200_OK)

class TicketDeleteView(APIView):
    def delete(self, request, *args, **kwargs):
        ticket_id = request.data.get('ticket-id')
        
        if ticket_id is None or ticket_id not in TicketModel.objects.values_list('id', flat=True):
            return Response({"error": "No or not existing ticket ID provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            TicketModel.objects.get(id=ticket_id).delete()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response({"status": "success"}, status=status.HTTP_200_OK)
    

class ErrorStatusView(APIView):
    def get(self, request):
        ticket_id = int(request.query_params.get('ticket-id'))
        if ticket_id is None or ticket_id not in TicketModel.objects.values_list('ticket_id', flat=True):
            return Response({"error": "No or not existing ticket ID provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            error = ErrorModel.objects.all().filter(ticket_id=ticket_id)
        except ErrorModel.DoesNotExist:
            return Response({"error": "No error found for the provided ticket ID"}, status=status.HTTP_404_NOT_FOUND)
        
        send_results = request.query_params.get('send-results')

        try:
            transcript = json.loads(open(f"data/transcripts/{ticket_id}.json").read())
        except:
            transcript = ""
        
        status_ = {}
        status_["transcription"] = transcript

        for err in error:
            if not err.name in status_:
                status_[err.name] = {"gaps": []}
            status_[err.name]["gaps"].append({"start": err.timestamp_start, "end": err.timestamp_end})

        return Response(status_, status=status.HTTP_200_OK)
        


@api_view(["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS", "TRACE"])
def proxy_to_frontend(request, path):
    frontend_url = f"http://localhost:3000/{path}"
    headers = {key: value for key, value in request.headers.items()}
    headers["Host"] = "localhost:3000"  # Explicitly set Host header

    try:
        response = requests.request(
            method=request.method,
            url=frontend_url,
            data=request.body,
            params=request.GET,
            allow_redirects=True,
            timeout=10
        )
        return HttpResponse(
            response.content,
            status=response.status_code,
            content_type=response.headers.get("Content-Type", "text/plain"),
        )
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Error proxying to frontend: {str(e)}", status=500)




        
        
        

        


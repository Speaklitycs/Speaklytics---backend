from django.db import models
from analysis.analysis_base_class import AnalysisBaseClass
from analysis.analysis_mapper import AnalysisMapper
from analysis.audio.analysis_audio_base_class import AudioAnalysisBaseClass
from analysis.image.analysis_image_base_class import ImageAnalysisBaseClass
from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass
import os
import time
import json


class TicketModel(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    

class ErrorModel(models.Model):
    name = models.CharField(max_length=50, null=True)
    timestamp_start = models.FloatField(null=True)
    timestamp_end = models.FloatField(null=True)
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE, related_name='errors', null=True)
    is_finished = models.BooleanField(default=False)
    text = models.TextField(null=True)
    wpm = models.FloatField(null=True)
    gfi = models.FloatField(null=True)

    @classmethod
    def analyze(cls, analysis_type, ticket_id):
        ticket = TicketModel.objects.get(ticket_id=ticket_id)
        analysis_class: AnalysisBaseClass = AnalysisMapper().get_analysis_class(analysis_type)

        path = cls.path_chooser(analysis_class, ticket_id)
        result = analysis_class(path).analyze()

        def error_exists(ticket, analysis_type, start, end):
            return ErrorModel.objects.filter(
                ticket=ticket, 
                name=analysis_type, 
                timestamp_start=start, 
                timestamp_end=end
            ).exists()

        if analysis_type == "metrics":
            if not error_exists(ticket, analysis_type, None, None):
                error = ErrorModel(
                    ticket=ticket, 
                    name=analysis_type, 
                    is_finished=True, 
                    wpm=result["wpm"], 
                    gfi=result["gfi"]
                )
                error.save()
            return

        if analysis_type == "general_language_opinion":
            if not error_exists(ticket, analysis_type, None, None):
                error = ErrorModel(
                    ticket=ticket, 
                    name=analysis_type, 
                    is_finished=True, 
                    text=result["text"]
                )
                error.save()
            return

        if result["gaps"] == []:
            if not error_exists(ticket, analysis_type, None, None):
                error = ErrorModel(
                    ticket=ticket, 
                    name=analysis_type, 
                    is_finished=True
                )
                error.save()
            return

        for gap in result["gaps"]:
            if not error_exists(ticket, analysis_type, gap["start"], gap["end"]):
                error = ErrorModel(
                    ticket=ticket, 
                    name=analysis_type, 
                    is_finished=True, 
                    timestamp_start=gap["start"], 
                    timestamp_end=gap["end"]
                )
                error.save()

    @classmethod
    def path_chooser(cls, analysis_class, ticket_id):
        if issubclass(analysis_class, AudioAnalysisBaseClass):
            return f"data/audios/{ticket_id}.wav"
        elif issubclass(analysis_class, ImageAnalysisBaseClass):
            return f"data/videos/{ticket_id}.mp4"
        elif issubclass(analysis_class, NlpAnalysisBaseClass):
            return f"data/transcripts/{ticket_id}.json"
        else:
            raise Exception(f"Wrong analysis class: {type(analysis_class)}")

    
    
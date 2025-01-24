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
        ticket=TicketModel.objects.get(ticket_id=ticket_id)
        error = ErrorModel(ticket=ticket, name=analysis_type)
        error.save()
        analysis_class: AnalysisBaseClass = AnalysisMapper().get_analysis_class(analysis_type)

        path = cls.path_chooser(analysis_class, ticket_id)
        result = analysis_class(path).analyze()
        if analysis_type == "metrics":
            error = ErrorModel(ticket=ticket, name=analysis_type, is_finished=True, wpm=result["wpm"], gfi=result["gfi"])
            error.save()
            return
        if analysis_type == 'general_language_opinion':
            error = ErrorModel(ticket=ticket, name=analysis_type, is_finished=True, text=result["text"])
            error.save()
            return 

        print(analysis_type)
        if result["gaps"] == []:
            error.is_finished = True
            error.save()
            return
        error.timestamp_start = result["gaps"][0]["start"]
        error.timestamp_end = result["gaps"][0]["end"]
        error.is_finished = True
        error.save()
        if len(result["gaps"]) > 1:
            for gap in result["gaps"]:
                error = ErrorModel(ticket=ticket, name=analysis_type, 
                                   is_finished=True, timestamp_start=gap["start"], 
                                   timestamp_end=gap["end"])
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

    
    
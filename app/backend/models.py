from django.db import models
from analysis.analysis_base_class import AnalysisBaseClass
from analysis.analysis_mapper import AnalysisMapper
import os
import time

class TicketModel(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    

class ErrorModel(models.Model):
    name = models.CharField(max_length=50, null=True)
    timestamp_start = models.FloatField(null=True)
    timestamp_end = models.FloatField(null=True)
    ticket = models.ForeignKey(TicketModel, on_delete=models.CASCADE, related_name='errors', null=True)
    is_finished = models.BooleanField(default=False)

    @classmethod
    def analyze(cls, analysis_type, transcript_path, ticket_id):
        ticket=TicketModel.objects.get(ticket_id=ticket_id)
        error = ErrorModel(ticket=ticket, name=analysis_type)
        error.save()
        analysis_class: AnalysisBaseClass = AnalysisMapper().get_analysis_class(analysis_type)
        result = analysis_class(transcript_path).analyze()
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

    
    
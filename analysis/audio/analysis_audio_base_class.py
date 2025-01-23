import json
from analysis.analysis_base_class import AnalysisBaseClass
import librosa
import numpy as np

class AudioAnalysisBaseClass(AnalysisBaseClass):
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.y, self.sr = librosa.load(audio_path)
        self.error = ""
    
    def add_timestamps(self, time_ranges):
        response = {
            "error": self.error,
            "gaps": []
        }
        
        for start, end in time_ranges:
            response["gaps"].append({
                "start": float(start),
                "end": float(end)
            })
            
        return response 
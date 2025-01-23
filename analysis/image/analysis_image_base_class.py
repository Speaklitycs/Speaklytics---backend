import cv2
import mediapipe as mp
from analysis.analysis_base_class import AnalysisBaseClass

class ImageAnalysisBaseClass(AnalysisBaseClass):
    def __init__(self, video_path):
        self.video_path = video_path
        self.error = ""
        self.cap = cv2.VideoCapture(video_path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
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
        
    def __del__(self):
        if self.cap:
            self.cap.release() 
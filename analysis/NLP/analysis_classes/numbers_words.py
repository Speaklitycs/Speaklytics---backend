from analysis.analysis_base_class import AnalysisBaseClass
from analysis.NLP.gpt import analyze_speech
from speech2text.speech2text import Speech2Text

class NumbersDetection(AnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error_name = "jargon"
        

    def analyze(self):
        response = analyze_speech("", f"Find numbers in the transcript: {self.transcript_text}")
        print(response)
        response = self.add_timestamps(response)
        return response
    

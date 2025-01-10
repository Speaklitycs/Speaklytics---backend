from analysis.analysis_base_class import AnalysisBaseClass
from analysis.NLP.gpt import analyze_speech
from speech2text.speech2text import Speech2Text

class JargonDetection(AnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error_name = "jargon"
        

    def analyze(self):
        response = analyze_speech("", f"Find jargon words in the transcript: {self.transcript_text}")
        response = self.add_timestamps(response)
        return response
    
if __name__ == "__main__":
    jargon = JargonDetection("data/transcripts/89.json")
    jargon.analyze()
    
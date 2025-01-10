import json
from analysis.analysis_base_class import AnalysisBaseClass
from analysis.NLP.gpt import analyze_speech
from speech2text.speech2text import Speech2Text

class JargonDetection(AnalysisBaseClass):
    def __init__(self, transcript_path):
        with open(transcript_path, "r", encoding="utf-8") as transcript_file:
            self.transcript_with_timestamps = json.load(transcript_file)
            self.transcript_text = Speech2Text.read_transcript_from_json(transcript_path)
            self.error = "jargon"
        

    def analyze(self):
        errors = analyze_speech("", f"Find jargon words in the transcript: {self.transcript_text}")
        errors = [error.strip() for error in errors.strip().split("|") if error.strip()]
        print(errors)
        response = self.add_timestamps_nlp(errors)
        print(response)
        return response
    
if __name__ == "__main__":
    jargon = JargonDetection("data/transcripts/89.json")
    jargon.analyze()
    
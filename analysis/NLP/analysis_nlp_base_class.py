import json
from analysis.analysis_base_class import AnalysisBaseClass
from analysis.NLP.gpt import analyze_speech
from speech2text.speech2text import Speech2Text



PROMPT_PATH = "analysis/NLP/prompts.json"

class NlpAnalysisBaseClass(AnalysisBaseClass):

    def __init__(self, transcript_path):
        with open(transcript_path, "r", encoding="utf-8") as transcript_file:
            self.transcript_with_timestamps = json.load(transcript_file)
            self.transcript_text = Speech2Text.read_transcript_from_json(transcript_path)
        
        with open(PROMPT_PATH, "r", encoding="utf-8") as prompt_file:
            self.prompt = json.load(prompt_file)   
        
        self.error = ""
        self.system = ""


    def add_timestamps(self, errors):
        
        response = {
            "error": self.error,
            "gaps": []
        }

        starts, ends = set(), set() 

        for error in errors:
            error_words = error.split()
            start_word, end_word = error_words[0], error_words[-1]

            start, end = None, None

            for word in self.transcript_with_timestamps["words"]:
                if word["word"] == start_word and word["start"] not in starts:
                    start = word["start"]
                    starts.add(start)
                if word["word"] == end_word and word["end"] not in ends:
                    end = word["end"]
                    ends.add(end)

                if start is not None and end is not None:
                    break

            if start is not None and end is not None:
                response["gaps"].append({"start": start, "end": end})

        
        return response
    
    def analyze(self):
        errors = analyze_speech(self.system, self.transcript_text)
        errors = [error.strip() for error in errors.strip().split("|") if error.strip()]
        print(errors)
        response = self.add_timestamps(errors)
        return response
        
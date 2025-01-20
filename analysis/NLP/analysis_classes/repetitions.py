from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass

class RepetitionsDetection(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "repetitions"
        self.system = self.prompt[self.error]

    def add_timestamps(self, errors):
        response = {
            "error": self.error,
            "gaps": []
        }

        for error in errors:
            for word in self.transcript_with_timestamps["words"]:
                if word["word"] == error:
                    response["gaps"].append({"start": word["start"], "end": word["end"]})
        return response
    
if __name__ == "__main__":
    repetitions = RepetitionsDetection("data/transcripts/repetition_example.json")
    analysis = repetitions.analyze()
    print(analysis)
    
    
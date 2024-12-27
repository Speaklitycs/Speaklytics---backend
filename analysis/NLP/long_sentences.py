from analysis.analysis_base_class import AnalysisBaseClass

class LongSentencesDetection(AnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(self, LongSentencesDetection)
        self.error_name = "long_sentences"
        with open(transcript_path, "r", encoding="utf-8") as f:
            self.transcript = f.read()

    def analyze(self):
        return {
            "error": self.error_name,
            "gaps": [
            ]
        }
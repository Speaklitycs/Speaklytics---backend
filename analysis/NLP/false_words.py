from analysis.analysis_base_class import AnalysisBaseClass

class FalseWordsDetection(AnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(self, FalseWordsDetection)
        self.error_name = "false_words"
        with open(transcript_path, "r", encoding="utf-8") as f:
            self.transcript = f.read()

    def analyze(self):
        return {
            "error": self.error_name,
            "gaps": [
            ]
        }
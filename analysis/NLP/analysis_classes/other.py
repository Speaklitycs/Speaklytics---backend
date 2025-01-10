from analysis.analysis_base_class import AnalysisBaseClass

class OtherErrorsDetection(AnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(self, OtherErrorsDetection)
        self.error_name = "other"
        with open(transcript_path, "r", encoding="utf-8") as f:
            self.transcript = f.read()

    def analyze(self):
        return {
            "error": self.error_name,
            "gaps": [
            ]
        }
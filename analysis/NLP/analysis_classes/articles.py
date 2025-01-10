from analysis.analysis_base_class import AnalysisBaseClass
import time

class ArticlesDetection(AnalysisBaseClass):
    def __init__(self, transcript_path):
        self.error_name = "articles"
        with open(transcript_path, "r", encoding="utf-8") as f:
            self.transcript = f.read()

    def analyze(self):
        time.sleep(10)
        return {
            "error": self.error_name,
            "gaps": [{"start": 0.125, 
                      "end": 1.07},
                     {"start": 2.125,
                      "end": 3.07}
            ]
        }
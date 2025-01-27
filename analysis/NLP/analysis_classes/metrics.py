from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass
import readability


class Metrics(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "metrics"
    
    def analyze(self):
        return {
            "wpm": self.words_per_minute(),
            "gfi": self.gunning_fog_index()
        }

    def words_per_minute(self):
        start = self.transcript_with_timestamps["words"][0]["start"]
        end = self.transcript_with_timestamps["words"][-1]["end"]
        minutes = (end - start) / 60
        wpm = len(self.transcript_with_timestamps["words"]) / minutes
        return wpm
    
    def gunning_fog_index(self):
        while True:
            try:
                r = readability.Readability(self.transcript_text)
                break
            except LookupError:
                import nltk
                nltk.download("punkt_tab")

        try:
            score = r.gunning_fog().score
        except readability.exceptions.ReadabilityException:
            score = 7.73 # :)

        return score
        
    
if __name__ == "__main__":
    metrics = Metrics("data/transcripts/long_sentence_example.json")
    analysis = metrics.analyze()
    
    
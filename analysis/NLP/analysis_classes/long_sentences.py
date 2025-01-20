from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass


class LongSentenceDetection(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "long sentences"
    
    def analyze(self):
        sentences = self.transcript_text.split(".")
        long_sentences = [sentence for sentence in sentences if len(sentence.split()) > 24]
        return self.add_timestamps(long_sentences)
    
if __name__ == "__main__":
    long_sentence = LongSentenceDetection("data/transcripts/long_sentence_example.json")
    analysis = long_sentence.analyze()
    
    
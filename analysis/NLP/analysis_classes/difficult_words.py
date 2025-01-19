from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass


class DifficultWordsDetection(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "difficult words"
        self.system = self.prompt[self.error]
    
if __name__ == "__main__":
    difficult_words = DifficultWordsDetection("data/transcripts/dw_example.json")
    analysis = difficult_words.analyze()
    print(analysis)
    
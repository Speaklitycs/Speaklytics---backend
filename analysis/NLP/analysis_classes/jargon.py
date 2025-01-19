from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass


class JargonDetection(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "jargon"
        self.system = self.prompt[self.error]
    
if __name__ == "__main__":
    jargon = JargonDetection("data/transcripts/jargon_example.json")
    analysis = jargon.analyze()
    print(analysis)
    
from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass
from analysis.NLP.gpt import analyze_speech


class GeneralLanguageOpinion(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "general_language_opinion"
        self.system = self.prompt[self.error]

    def analyze(self):
        opinion = analyze_speech(self.system, self.transcript_text)
        return {
            "text": opinion
        }
    
if __name__ == "__main__":
    language_opinion = GeneralLanguageOpinion("data/transcripts/jargon_example.json")
    analysis = language_opinion.analyze()
    
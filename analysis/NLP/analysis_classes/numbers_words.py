from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass

class NumbersDetection(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "numbers"
    
    def analyze(self):
        words = self.transcript_text.split()
        numbers = [word for word in words if word.isdigit()]
        return self.add_timestamps(numbers)
    
if __name__ == "__main__":
    numbers = NumbersDetection("data/transcripts/number_example.json")
    analysis = numbers.analyze()
    print(analysis)
    
    
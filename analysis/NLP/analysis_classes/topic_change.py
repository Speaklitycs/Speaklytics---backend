from analysis.NLP.analysis_nlp_base_class import NlpAnalysisBaseClass


class TopicChangeDetection(NlpAnalysisBaseClass):
    def __init__(self, transcript_path):
        super().__init__(transcript_path)
        self.error = "topic change"
        self.system = self.prompt[self.error]
    
if __name__ == "__main__":
    topic_change = TopicChangeDetection("data/transcripts/topic_change_example.json")
    analysis = topic_change.analyze()
    print(analysis)
    
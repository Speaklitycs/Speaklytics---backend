from analysis.NLP.analysis_classes.difficult_words import DifficultWordsDetection
from analysis.NLP.analysis_classes.jargon import JargonDetection
from analysis.NLP.analysis_classes.long_sentences import LongSentenceDetection
from analysis.NLP.analysis_classes.numbers_words import NumbersDetection
from analysis.NLP.analysis_classes.repetitions import RepetitionsDetection
from analysis.NLP.analysis_classes.topic_change import TopicChangeDetection

class WrongAnalysisTypeException(Exception):
    pass


class AnalysisMapper:
    def __init__(self):
        self.mapping = {
            "difficult_words": DifficultWordsDetection,
            "jargon": JargonDetection,
            "numbers": NumbersDetection,
            "topic_change": TopicChangeDetection,
            "repetition": RepetitionsDetection,
            "long_sentences": LongSentenceDetection
        }

    def get_analysis_class(self, analysis_type):
        if analysis_type not in self.mapping:
            raise WrongAnalysisTypeException(f"Analysis type {analysis_type} is not supported")
        return self.mapping.get(analysis_type)
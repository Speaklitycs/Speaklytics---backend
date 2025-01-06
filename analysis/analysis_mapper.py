from analysis.NLP.articles import ArticlesDetection
from analysis.NLP.difficult_words import DifficultWordsDetection
from analysis.NLP.false_words import FalseWordsDetection
from analysis.NLP.jargon import JargonDetection
from analysis.NLP.long_sentences import LongSentencesDetection
from analysis.NLP.numbers import NumbersDetection
from analysis.NLP.other import OtherErrorsDetection
from analysis.NLP.repetitions import RepetitionDetection
from analysis.NLP.topic_change import TopicChangeDetection

class WrongAnalysisTypeException(Exception):
    pass


class AnalysisMapper:
    def __init__(self):
        self.mapping = {
            "articles": ArticlesDetection,
            "difficult_words": DifficultWordsDetection,
            "false_words": FalseWordsDetection,
            "jargon": JargonDetection,
            "long_sentences": LongSentencesDetection,
            "numbers": NumbersDetection,
            "other": OtherErrorsDetection,
            "repetitions": RepetitionDetection,
            "topic_change": TopicChangeDetection
        }

    def get_analysis_class(self, analysis_type):
        if analysis_type not in self.mapping:
            raise WrongAnalysisTypeException(f"Analysis type {analysis_type} is not supported")
        return self.mapping.get(analysis_type)
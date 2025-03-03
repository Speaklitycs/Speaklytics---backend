from analysis.NLP.analysis_classes.difficult_words import DifficultWordsDetection
from analysis.NLP.analysis_classes.jargon import JargonDetection
from analysis.NLP.analysis_classes.long_sentences import LongSentenceDetection
from analysis.NLP.analysis_classes.numbers_words import NumbersDetection
from analysis.NLP.analysis_classes.repetitions import RepetitionsDetection
from analysis.NLP.analysis_classes.topic_change import TopicChangeDetection
from analysis.audio.analysis_classes.silence_detection import SilenceDetection
from analysis.audio.analysis_classes.volume_detection import VolumeDetection
from analysis.image.analysis_classes.background_people_detection import BackgroundPeopleDetection
from analysis.image.analysis_classes.excessive_gestures_detection import ExcessiveGesturesDetection
from analysis.NLP.analysis_classes.general_language_opinion import GeneralLanguageOpinion
from analysis.NLP.analysis_classes.metrics import Metrics

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
            "long_sentences": LongSentenceDetection,
            "general_language_opinion": GeneralLanguageOpinion,
            "metrics": Metrics,
            "silence": SilenceDetection,
            "volume": VolumeDetection,
            "background_people": BackgroundPeopleDetection,
            "excessive_gestures": ExcessiveGesturesDetection
        }

    def get_analysis_class(self, analysis_type):
        if analysis_type not in self.mapping:
            raise WrongAnalysisTypeException(f"Analysis type {analysis_type} is not supported")
        return self.mapping.get(analysis_type)
    
    def get_all_analysis_types(self):
        return list(self.mapping.keys())

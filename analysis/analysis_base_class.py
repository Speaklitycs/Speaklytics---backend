from abc import ABC, abstractmethod

class AnalysisBaseClass(ABC):
    def __init__(self):
        super().__init__(self, AnalysisBaseClass)

    @abstractmethod
    def analyze(self):
        """
    Analyzes the data.

    Returns:
        list[dict] - A list of dictionaries containing the analysis results, one for every error.
        Dict should follow this json structure:
        {
            "error": error type,
            "timestamp_start": start timestamp (in seconds)
            "timestamp_end": end timestamp (in seconds),
        }
    """
        raise NotImplementedError("Analyze method not implemented")
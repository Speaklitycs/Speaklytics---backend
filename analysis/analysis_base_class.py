from abc import ABC, abstractmethod
from speech2text.speech2text import Speech2Text

class AnalysisBaseClass(ABC):

    @abstractmethod
    def analyze(self) -> dict["error": str, 
                              "gaps": list[dict["start": float, "end": float]]]:
        """
    Analyzes the data.

    Returns:
        dict: A dictionary containing the error message, start timestamps, and end timestamps.
        The structure of the dictionary is as follows:
        {
            "error": "An error message",
            "gaps": [
                {
                    "start": 0.125,
                    "end": 1.07
                }
            ]
        }
    """
        raise NotImplementedError("Analyze method not implemented")
    
    


        
from abc import ABC, abstractmethod
import json
from speech2text.speech2text import Speech2Text

class AnalysisBaseClass(ABC):

    @abstractmethod
    def __init__(self, transcript_path: str):
        with open(transcript_path, "r", encoding="utf-8") as transcript_file:
            self.transcript_with_timestamps = json.load(transcript_file)
        self.transcript_text = Speech2Text.read_transcript_from_json(transcript_path)
        self.error = ""

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
    
    def add_timestamps(self, errors):
        errors = [error.strip() for error in errors.strip().split("|") if error.strip()]
        response = {
            "error": self.error,
            "gaps": []
        }

        starts, ends = set(), set()  # Use sets to efficiently track seen timestamps

        for error in errors:
            error_words = error.split()
            start_word, end_word = error_words[0], error_words[-1]

            start, end = None, None

            for word in self.transcript_with_timestamps["words"]:
                if word["word"] == start_word and word["start"] not in starts:
                    start = word["start"]
                    starts.add(start)
                if word["word"] == end_word and word["end"] not in ends:
                    end = word["end"]
                    ends.add(end)

                if start is not None and end is not None:
                    break

            if start is not None and end is not None:
                response["gaps"].append({"start": start, "end": end})

        
        print(response)
        return response
        


        
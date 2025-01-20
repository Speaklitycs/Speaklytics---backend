from openai import OpenAI
from dotenv import load_dotenv
import json
import os
load_dotenv()


class Whisper:
    def __init__(self, audio_path, model="whisper-1", api_key=os.getenv("OPENAI_API_KEY")):
        self.audio_path = audio_path
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def transcribe(self):
        with open(self.audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
            text_transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file,
            response_format="text"
        )
        result = {"words": [], "text": ""}
        for word in transcription.words:
            result["words"].append({
                "word": word.word,
                "start": word.start,
                "end": word.end
            })
        result["text"] = text_transcription
        return result


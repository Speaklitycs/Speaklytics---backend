from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


class Whisper:
    def __init__(self, audio_path, model="whisper-1", api_key=os.getenv("OPENAI_API_KEY")):
        self.audio_path = audio_path
        self.model = model
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def transcribe(self):
        audio_file = open(self.audio_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            model=self.model,
            file=audio_file)
        return transcription.text
        

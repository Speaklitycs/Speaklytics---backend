from speech2text.audio_extractor import AudioExtractor
from speech2text.whisper import Whisper

class Speech2Text:
    def __init__(self, video_path, audio_path):
        self.audio_path = audio_path
        self.audio_extractor = AudioExtractor(video_path, audio_path)
        self.whisper = Whisper(audio_path)

    def extract_transcript(self):
        self.audio_extractor.extract_audio()
        return self.whisper.transcribe()

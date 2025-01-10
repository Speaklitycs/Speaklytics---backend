import json
from speech2text.audio_extractor import AudioExtractor
from speech2text.whisper import Whisper

class Speech2Text:
    def __init__(self, video_path, audio_path, transcript_path):
        if not video_path.endswith('.mp4'):
            raise ValueError('Input video must be in .mp4 format.')
        if not audio_path.endswith('.wav'):
            raise ValueError('Output audio must be in .wav format.')
        if not transcript_path.endswith('.json'):
            raise ValueError('Output transcript must be in .json format.')
        self.audio_path = audio_path
        self.transcript_path = transcript_path
        self.audio_extractor = AudioExtractor(video_path, audio_path)
        self.whisper = Whisper(audio_path)

    def extract_transcript_and_audio(self):
        self.audio_extractor.extract_audio()
        transcript = self.whisper.transcribe()
        self.save_transcript(transcript)

    def save_transcript(self, transcript):
        with open(self.transcript_path, 'w', encoding='UTF-8') as f:
            json.dump(transcript, f, ensure_ascii=False, indent=4)

    @classmethod
    def read_transcript_from_json(cls, transcript_path):
        with open(transcript_path, 'r', encoding='UTF-8') as f:
            data = json.load(f)
        transcript = ""
        for item in data["words"]:
            transcript += item['word']
            transcript += " "
        return transcript
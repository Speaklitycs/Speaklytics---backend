from speech2text.audio_extractor import AudioExtractor
from speech2text.whisper import Whisper

class Speech2Text:
    def __init__(self, video_path, audio_path, transcript_path):
        if not video_path.endswith('.mp4'):
            raise ValueError('Input video must be in .mp4 format.')
        if not audio_path.endswith('.wav'):
            raise ValueError('Output audio must be in .wav format.')
        if not transcript_path.endswith('.txt'):
            raise ValueError('Output transcript must be in .txt format.')
        self.audio_path = audio_path
        self.transcript_path = transcript_path
        self.audio_extractor = AudioExtractor(video_path, audio_path)
        self.whisper = Whisper(audio_path)

    def extract_transcript(self):
        self.audio_extractor.extract_audio()
        transcript = self.whisper.transcribe()

    def save_transcript(self, transcript):
        with open(self.transcript_path, 'w') as f:
            f.write(transcript)
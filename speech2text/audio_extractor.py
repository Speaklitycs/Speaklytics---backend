from moviepy import VideoFileClip


class AudioExtractor:
    def __init__(self, video_path, audio_path):
        self.video_path = video_path
        self.audio_path = audio_path

    def extract_audio(self):
        video = VideoFileClip(self.video_path)
        audio = video.audio
        audio.write_audiofile(self.audio_path)
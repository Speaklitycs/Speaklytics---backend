from moviepy.video.io.VideoFileClip import VideoFileClip


class AudioExtractor:
    """
    Extract audio from a video file and save it as a .wav file.
    """
    def __init__(self, video_path: str, audio_path: str):
        self.video_path = video_path
        self.audio_path = audio_path

    def extract_audio(self):
        video = VideoFileClip(self.video_path)
        audio = video.audio
        audio.write_audiofile(self.audio_path)
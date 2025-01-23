from analysis.audio.analysis_audio_base_class import AudioAnalysisBaseClass
import librosa
import numpy as np

class SilenceDetection(AudioAnalysisBaseClass):
    def __init__(self, audio_path, min_silence_duration=1.0, silence_threshold=-60):
        super().__init__(audio_path)
        self.error = "silence"
        self.min_silence_duration = min_silence_duration
        self.silence_threshold = silence_threshold
    
    def analyze(self):
        # Convert to dB
        db = librosa.amplitude_to_db(np.abs(self.y), ref=np.max)
        
        # Find silent regions
        is_silent = db < self.silence_threshold
        
        # Find silence boundaries
        silent_regions = []
        start = None
        
        for i in range(len(is_silent)):
            if is_silent[i] and start is None:
                start = i / self.sr
            elif not is_silent[i] and start is not None:
                end = i / self.sr
                if end - start >= self.min_silence_duration:
                    silent_regions.append((start, end))
                start = None
                
        return self.add_timestamps(silent_regions)

if __name__ == "__main__":
    silence = SilenceDetection("data/audios/example.wav")
    analysis = silence.analyze()
    print(analysis) 
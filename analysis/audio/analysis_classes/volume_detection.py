from analysis.audio.analysis_audio_base_class import AudioAnalysisBaseClass
import librosa
import numpy as np

class VolumeDetection(AudioAnalysisBaseClass):
    def __init__(self, audio_path, window_size=1.0, low_threshold=-35, high_threshold=-10):
        super().__init__(audio_path)
        self.error = "volume"
        self.window_size = window_size
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold
    
    def analyze(self):
        # Convert to dB
        db = librosa.amplitude_to_db(np.abs(self.y), ref=np.max)
        
        # Calculate window size in samples
        window_samples = int(self.window_size * self.sr)
        
        # Analyze volume in windows
        volume_issues = []
        for i in range(0, len(db), window_samples):
            window = db[i:i+window_samples]
            avg_volume = np.mean(window)
            
            start_time = i / self.sr
            end_time = min((i + window_samples) / self.sr, len(self.y) / self.sr)
            
            if avg_volume < self.low_threshold:
                volume_issues.append((start_time, end_time))
            elif avg_volume > self.high_threshold:
                volume_issues.append((start_time, end_time))
                
        return self.add_timestamps(volume_issues)

if __name__ == "__main__":
    volume = VolumeDetection("data/audios/example.wav")
    analysis = volume.analyze()
    print(analysis) 
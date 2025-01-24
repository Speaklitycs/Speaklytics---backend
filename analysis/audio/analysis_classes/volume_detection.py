from analysis.audio.analysis_audio_base_class import AudioAnalysisBaseClass
import librosa
import numpy as np

class VolumeDetection(AudioAnalysisBaseClass):
    def __init__(self, audio_path, low_threshold_offset=-20, high_threshold_offset=15):
        super().__init__(audio_path)
        self.error = "volume"
        self.low_threshold_offset = low_threshold_offset  # dB below median
        self.high_threshold_offset = high_threshold_offset  # dB above median
    
    def analyze(self):
        # Convert to dB
        db = librosa.amplitude_to_db(np.abs(self.y), ref=np.max)
        
        # Calculate median volume level
        median_volume = np.median(db)
        
        # Set thresholds relative to median
        self.low_threshold = median_volume + self.low_threshold_offset
        self.high_threshold = median_volume + self.high_threshold_offset
        
        # Find volume issues
        volume_issues = []
        start = None
        prev_is_issue = False
        
        for i in range(len(db)):
            current_time = i / self.sr
            is_issue = db[i] < self.low_threshold or db[i] > self.high_threshold
            
            if is_issue and not prev_is_issue:
                start = current_time
            elif not is_issue and prev_is_issue:
                volume_issues.append((start, current_time))
                start = None
                
            prev_is_issue = is_issue
        
        # Handle case where file ends during an issue
        if start is not None:
            volume_issues.append((start, len(self.y) / self.sr))
                
        return self.add_timestamps(volume_issues)

if __name__ == "__main__":
    volume = VolumeDetection("data/audios/example.wav")
    analysis = volume.analyze()
    print(analysis)

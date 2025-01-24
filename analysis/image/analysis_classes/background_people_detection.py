import cv2
import mediapipe as mp
from analysis.image.analysis_image_base_class import ImageAnalysisBaseClass

class BackgroundPeopleDetection(ImageAnalysisBaseClass):
    def __init__(self, video_path, detection_threshold=0.5, min_duration=1.0):
        super().__init__(video_path)
        self.error = "background_people"
        self.detection_threshold = detection_threshold
        self.min_duration = min_duration
        self.mp_pose = mp.solutions.pose
        
    def analyze(self):
        background_periods = []
        current_start = None
        frame_count = 0
        
        with self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if not success:
                    break
                    
                current_time = frame_count / self.fps
                frame_count += 1
                
                # Convert BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)
                
                if results.pose_landmarks:
                    # Count detected poses
                    num_people = len([landmark for landmark in results.pose_landmarks.landmark 
                                    if landmark.visibility > self.detection_threshold])
                    
                    if num_people > 1:  # More than one person detected
                        if current_start is None:
                            current_start = current_time
                    elif current_start is not None:
                        duration = current_time - current_start
                        if duration >= self.min_duration:
                            background_periods.append((current_start, current_time))
                        current_start = None
            
            # Handle case where video ends during a detection period
            if current_start is not None:
                duration = frame_count/self.fps - current_start
                if duration >= self.min_duration:
                    background_periods.append((current_start, frame_count/self.fps))
                    
        #return self.add_timestamps(background_periods)
        return {"gaps": [{
            "start": None,
            "end": None
        }]}

if __name__ == "__main__":
    detector = BackgroundPeopleDetection("data/videos/example.mp4")
    analysis = detector.analyze()
    print(analysis)
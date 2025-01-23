import cv2
import mediapipe as mp
import numpy as np
from analysis.image.analysis_image_base_class import ImageAnalysisBaseClass

class ExcessiveGesturesDetection(ImageAnalysisBaseClass):
    def __init__(self, video_path, movement_threshold=0.3, window_size=30):
        super().__init__(video_path)
        self.error = "excessive_gestures"
        self.movement_threshold = movement_threshold
        self.window_size = window_size  # frames to analyze movement
        self.mp_holistic = mp.solutions.holistic
        
    def calculate_movement(self, prev_landmarks, curr_landmarks):
        if not prev_landmarks or not curr_landmarks:
            return 0
            
        # Calculate movement for hands and arms
        movement = 0
        hand_indices = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]  # Hand and arm landmarks
        
        for idx in hand_indices:
            prev = prev_landmarks[idx]
            curr = curr_landmarks[idx]
            movement += np.sqrt((curr.x - prev.x)**2 + 
                              (curr.y - prev.y)**2 + 
                              (curr.z - prev.z)**2)
            
        return movement / len(hand_indices)
    
    def analyze(self):
        excessive_periods = []
        current_start = None
        frame_count = 0
        prev_landmarks = None
        movement_buffer = []
        
        with self.mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic:
            
            while self.cap.isOpened():
                success, frame = self.cap.read()
                if not success:
                    break
                    
                current_time = frame_count / self.fps
                frame_count += 1
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(frame_rgb)
                
                if results.pose_landmarks:
                    movement = self.calculate_movement(
                        prev_landmarks, 
                        results.pose_landmarks.landmark
                    )
                    movement_buffer.append(movement)
                    
                    if len(movement_buffer) >= self.window_size:
                        avg_movement = sum(movement_buffer) / len(movement_buffer)
                        
                        if avg_movement > self.movement_threshold:
                            if current_start is None:
                                current_start = current_time - (self.window_size / self.fps)
                        elif current_start is not None:
                            excessive_periods.append((current_start, current_time))
                            current_start = None
                            
                        movement_buffer.pop(0)
                    
                    prev_landmarks = results.pose_landmarks.landmark
            
            # Handle case where video ends during excessive movement
            if current_start is not None:
                excessive_periods.append((current_start, frame_count/self.fps))
                    
        return self.add_timestamps(excessive_periods)

if __name__ == "__main__":
    detector = ExcessiveGesturesDetection("data/videos/example.mp4")
    analysis = detector.analyze()
    print(analysis)
    
from IConsumer import IConsumer
import cv2

class DrawBoxConsumer(IConsumer):
    def process_frame(self, frame):
        frame = cv2.rectangle(frame, (20, 20), (100,100), (255, 0, 0), 2)
        return frame
    
    def process_frames(self, frames):
        return next(iter(frames.values()))
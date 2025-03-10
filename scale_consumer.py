from IConsumer import IConsumer
import cv2

class ScaleConsumer(IConsumer):
    def __init__(self, ratio):
        self.ratio = ratio

    def process_frame(self, frame):
        frame = cv2.resize(frame,
            (0,0),
            fx=self.ratio, 
            fy=self.ratio, 
            interpolation=cv2.INTER_NEAREST)
        return frame
    
    def process_frames(self, frames):
        return self.process_frame(next(iter(frames.values())))
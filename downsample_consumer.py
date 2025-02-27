from consumer_mpq import Consumer
import cv2

class DownsampleConsumer(Consumer):
    def __init__(self, name, ratio):
        super().__init__(name,)
        self.ratio = ratio

    def process_frame(self, frame):
        frame = cv2.resize(frame,
            (0,0),
            fx=self.ratio, 
            fy=self.ratio, 
            interpolation=cv2.INTER_NEAREST)
        return frame
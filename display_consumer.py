from IConsumer import IConsumer

class DisplayConsumer(IConsumer):
    def process_frame(self, frame):
        return frame
    
    def process_frames(self, frames):
        return next(iter(frames.values()))
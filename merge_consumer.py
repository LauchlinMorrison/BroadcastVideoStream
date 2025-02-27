from consumer_mpq import Consumer
import cv2
import numpy as np

class MergeConsumer(Consumer):
    def __init__(self, name):
        super().__init__(name,)

    def process_frames(self, frames):
        
        img1 = frames["camera"]
        img2 = frames["video"]

        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]

        #create empty matrix
        frame = np.zeros((max(h1, h2), w1+w2,3), np.uint8)

        #combine 2 images
        frame[:h1, :w1,:3] = img1
        frame[:h2, w1:w1+w2,:3] = img2

        return frame
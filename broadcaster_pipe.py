import multiprocessing
import cv2
import threading
import time

class Broadcast:
    def __init__(self, name, source=0):
        self.name = name
        self._pipes = {}
        self.source = source

    def subscribe(self, consumer):
        name = consumer.name
        if name in self._pipes:
            raise Exception(f"Already subscribed to this broadcast.")
        else:
            rec, send = multiprocessing.Pipe()
            self._pipes[name] = send
            consumer.subscribe(self.name, rec)
        
    def unsubscribe(self, name):
        if name in self._pipes:
            del self._pipes[name]
        else:
            raise Exception(f"Cannot unsubscribe as it isn't subscribed.")
        
    def broadcast_worker(self):
        capture = cv2.VideoCapture(self.source)
        fps = capture.get(cv2.CAP_PROP_FPS)
        print(f"Source FPS: {fps}")
        
        while True:
            ret, frame = capture.read()

            for key, pipe in self._pipes.items():
                pipe.send(frame)
            
            time.sleep(1/fps)
        capture.release()

    def start(self):
        """Start the broadcast process."""
        thread = threading.Thread(target=self.broadcast_worker)
        thread.start()
        return thread
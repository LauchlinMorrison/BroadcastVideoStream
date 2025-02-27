import multiprocessing
import cv2
import threading
import time

class Broadcast:
    def __init__(self, name, source=0):
        self.name = name
        self._queues = {}
        self.source = source

    def assign(self, name):
        if name in self._queues:
            raise Exception(f"Name [{name}] already assigned to broadcast.")
        else:
            self._queues[name] = multiprocessing.Queue(maxsize=10)
            return self._queues[name]
        
    def unassign(self, name):
        if name in self._queues:
            del self._queues[name]
        else:
            raise Exception(f"Name [{name}] cannot be unassigned as it isn't assigned.")
        
    def broadcast_worker(self):
        capture = cv2.VideoCapture(self.source)
        fps = capture.get(cv2.CAP_PROP_FPS)
        print(f"Source FPS: {fps}")
        
        while True:
            ret, frame = capture.read()

            for key, queue in self._queues.items():
                queue.put(frame)
            
            time.sleep(1/fps)
        capture.release()

    def start(self):
        """Start the broadcast process."""
        thread = threading.Thread(target=self.broadcast_worker)
        thread.start()
        return thread
import multiprocessing
import cv2
import threading
import time

class Broadcast:
    def __init__(self, name, source=0):
        self.name = name
        self._queues = {}
        self.source = source

    def attach(self, consumer):
        if consumer.name in self._queues:
            raise Exception(f"Already attached to this consumer.")
        else:
            self._queues[consumer.name] = multiprocessing.Queue(maxsize=10)
            return self._queues[consumer.name]
        
    def remove(self, consumer):
        if consumer.name in self._queues:
            del self._queues[consumer.name]
            print("Unsubbed")
        else:
            raise Exception(f"Cannot remove as it isn't attached.")
        
    def broadcast_worker(self):
        capture = cv2.VideoCapture(self.source)
        fps = capture.get(cv2.CAP_PROP_FPS)
        print(f"Source FPS: {fps}")
        
        while True:
            ret, frame = capture.read()

            for key, queue in self._queues.items():
                if not queue.full():
                    queue.put(frame)
            
            time.sleep(1/fps)
        capture.release()

    def start(self):
        """Start the broadcast process."""
        thread = threading.Thread(target=self.broadcast_worker)
        thread.start()
        return thread
import multiprocessing
import cv2
import time

class Consumer:
    def __init__(self, name, logic):
        self.name = name
        self._queues = {}
        self._frames = {}
        self._display = True
        self._show_fps = True
        self._last_frame_time = None
        self._fps_history = [0]* 40
        self._fps_history_iter = 0
        self._fps = 0
        self._avg_fps = 0
        self._connected_nodes = []
        self.logic = logic

    def subscribe(self, broadcast):
        if broadcast.name in self._queues:
            raise Exception("Already subscribed to this broadcast.")
        else:
            self._queues[broadcast.name] = broadcast.attach(self)
            self._connected_nodes.append(broadcast)
    
    def unsubscribe(self, broadcast):
        if broadcast.name in self._queues:
            del self._queues[broadcast.name]
            broadcast.remove(self)
            if broadcast.name in self._frames:
                del self._frames[broadcast.name]
        else:
            raise Exception("Cannot unsubscribe as it isn't subscribed.")
    
    def __unsubscribe_all(self):
        for node in self._connected_nodes:
            self.unsubscribe(node)

    def consumer_worker(self):
        while True:
            updateFPS = True
            for key, queue in self._queues.items():
                if not queue.empty():
                    self._frames[key] = queue.get()
                    if updateFPS: self.__update_fps()
                    updateFPS = False

            if self._frames:
                frame = self.logic.process_frames(self._frames) if len(self._frames) > 1 else self.logic.process_frame(next(iter(self._frames.values())))
                
                if self._display:
                    self.__display(frame)
                    # Press ESC key or close window to stop consumer.
                    if cv2.waitKey(1) == 27:
                        break
        cv2.destroyWindow(self.name)
        self.__unsubscribe_all()

    def __display(self, frame):
        if self._show_fps: self.__draw_fps(frame)
        cv2.imshow(f'{self.name}', frame)

    def __draw_fps(self, frame):
        cv2.putText(frame, 
            f"FPS: {self._fps}", 
            (5, 25), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (255,0,255), 
            2, 
            cv2.LINE_AA)
        
    def __update_fps(self):
        frameTime = time.time()
        deltaTime = frameTime-self._last_frame_time if self._last_frame_time is not None else 1
        self._last_frame_time = frameTime
        fps = int(1/deltaTime)
        self._fps_history[self._fps_history_iter] = fps
        self._fps_history_iter+=1
        if self._fps_history_iter == len(self._fps_history): self._fps_history_iter=0
        self._fps = fps
        self._avg_fps = sum(self._fps_history) / len(self._fps_history)

    def start(self):
        """Start the consumer process."""
        process = multiprocessing.Process(target=self.consumer_worker)
        process.start()
        return process
import multiprocessing
import multiprocessing.queues
import time
import cv2

class Node(multiprocessing.Process):
    def __init__(self, node_id, ledger, source=None, consumer_logic=None):
        super(Node, self).__init__()
        self.id = node_id
        self.ledger = ledger
        self.source = source
        self.exit = multiprocessing.Event()
        self.frames_in = {}
        self.frame_out = None
        self.consumer_logic = consumer_logic
        self.display = True
        self.show_fps = True
        self.last_frame_time = None
        self.fps_history = [0]* 40
        self.fps_history_iter = 0
        self.fps = 0
        self.avg_fps = 0

    def __update_fps(self):
        frameTime = time.time()
        deltaTime = frameTime-self.last_frame_time if self.last_frame_time is not None else 1
        self.last_frame_time = frameTime
        fps = int(1/deltaTime)
        self.fps_history[self.fps_history_iter] = fps
        self.fps_history_iter+=1
        if self.fps_history_iter == len(self.fps_history): self.fps_history_iter=0
        self.fps = fps
        self.avg_fps = sum(self.fps_history) / len(self.fps_history)
    
    def __draw_fps(self, frame):
        cv2.putText(frame, 
            f"FPS: {self.fps}", 
            (5, 25), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (255,0,255), 
            2, 
            cv2.LINE_AA)

    def __display(self, frame):
        if self.show_fps: self.__draw_fps(frame)
        cv2.imshow(f'{self.id}', frame)
        # Press ESC key or close window to stop consumer.
        if cv2.waitKey(1) == 27:
            self.exit.set()
            cv2.destroyWindow(self.id)

    def __consume(self):
        if self.ledger[self.id]["broadcasts"]:
            updateFPS = True
            for broadcast_id, broadcast_queue in self.ledger[self.id]["broadcasts"].items():
                if not broadcast_queue.empty():
                    self.frames_in[broadcast_id] = broadcast_queue.get()
                    if updateFPS: self.__update_fps()
                    updateFPS = False

            if self.frames_in:
                self.frame_out = self.consumer_logic.process_frames(self.frames_in) if len(self.frames_in) > 1 else self.consumer_logic.process_frame(next(iter(self.frames_in.values())))
                if self.display:
                    self.__display(self.frame_out)
                
    def __broadcast(self, capture, fps):
        if self.ledger[self.id]["consumers"]:
            for consumer_id, consumer_queue in self.ledger[self.id]["consumers"].items():
                if not consumer_queue.full():
                    ret, frame_out = capture.read()
                    consumer_queue.put(frame_out)
                    time.sleep(1/fps)
    
    def __re_broadcast(self):
        if self.ledger[self.id]["consumers"]:
            for consumer_id, consumer_queue in self.ledger[self.id]["consumers"].items():
                if not consumer_queue.full():
                    if self.frame_out is not None:
                        consumer_queue.put(self.frame_out)
    
    # def __clear_frames(self):
    #     for id, frame in self.frames_in.items():
    #         if id not in [self.id]["broadcasts"]:
    #             del self.frames_in[id]

    def run(self):
        if self.source is not None and self.source != "re-broadcast":
            capture = cv2.VideoCapture(self.source)
            fps = capture.get(cv2.CAP_PROP_FPS)

        self.exit.clear()
        while not self.exit.is_set():
            if self.id in self.ledger:

                # Consumer logic
                if self.consumer_logic is not None:
                    self.__consume()

                # Broadcast logic
                if self.source is not None:
                    if self.source == "re-broadcast":
                        self.__re_broadcast()
                    else:
                        self.__broadcast(capture, fps)

            #self.__clear_frames()
        print(f"[{self.id}] node process ended.")

    def stop(self):
        self.exit.set()
import socket
import struct
import cv2
import numpy as np
import multiprocessing
import time

class Consumer:
    def __init__(self, name, multicast_port=5000, multicast_ip="224.1.1.1"):
        self.name = name
        self.multicast_ip = multicast_ip
        self.multicast_port = multicast_port
        self._display_fps = False
        self._last_frame_time = None
        self._fps_history = [0]* 40
        self._fps_history_iter = 0

    def set_multicast_address(self, port, ip="224.1.1.1"):
        """Set the UDP multicast address. (Port & IP)"""
        self.multicast_port = port
        self.multicast_ip = ip
    
    def display_fps(self, isDisplayed=True):
        """Set the display FPS state."""
        self._display_fps = isDisplayed

    def __draw_fps(self, frame):
        frameTime = time.time()
        deltaTime = frameTime-self._last_frame_time if self._last_frame_time is not None else 1
        self._last_frame_time = frameTime

        fps = int(1/deltaTime)
        self._fps_history[self._fps_history_iter] = fps
        self._fps_history_iter+=1
        if self._fps_history_iter == len(self._fps_history): self._fps_history_iter=0

        fpsAvg = sum(self._fps_history) / len(self._fps_history)
        cv2.putText(frame, f"FPS: {fpsAvg}", (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255), 2, cv2.LINE_AA)
        return frame
    
    def display_multicast_udp(self):
        BUFFERSIZE = 65536
        consumer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        consumer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        consumer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        consumer_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4096)
        group = socket.inet_aton(self.multicast_ip)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        consumer_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        consumer_socket.bind(("", self.multicast_port))

        print(f"Consumer listening for multicast messages on {self.multicast_ip}:{self.multicast_port}")

        chunk_list = []
        expected_chunks = 0
        
        while True:
            data, addr = consumer_socket.recvfrom(BUFFERSIZE)
            header = data[:8]
            chunk_data = data[8:]

            chunk_index, total_chunks = struct.unpack('!II', header)
            if expected_chunks == 0:
                expected_chunks = total_chunks
            chunk_list.append(chunk_data)

            # Decode and display if we've received all the data.
            if len(chunk_list) == expected_chunks:
                data = b''.join(chunk_list)
                np_arr = np.frombuffer(data, dtype=np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                if frame is not None:
                    if not self.__show_frame(frame): break

                chunk_list.clear()
                expected_chunks = 0

        consumer_socket.close()
        cv2.destroyAllWindows()
    
    def __show_frame(self, frame):
        """
        Performs any processing to the frame and display's it to the screen.
        Returns false if the process should end.
        """
        frame = self.process_frame(frame)
        if self._display_fps == True: frame = self.__draw_fps(frame)
        cv2.imshow(self.name, frame)

        # ESC key or close window to exit.
        if cv2.waitKey(1) == 27:
            return False
        if cv2.getWindowProperty(self.name ,cv2.WND_PROP_VISIBLE) < 1:
            return False
        return True

    def process_frame(self, frame):
        # override in children
        return frame
    
    def start(self):
        """Start the consumer process."""
        # Process over thread due to openCV shared gui objects not behaving correctly with threading.
        # Process doesn't seem to like starting private methods due to serialization so this one's remaining public for now.
        process = multiprocessing.Process(target=self.display_multicast_udp)
        process.start()
        return process
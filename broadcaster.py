import socket
import struct
import cv2
import time
import threading

class Broadcaster:

    def broadcast_udp_multicast(self, source=0, multicast_port=5000, multicast_ip='224.1.1.1'):
        CHUNKSIZE = 64000
        broadcaster_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        broadcaster_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        broadcaster_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

        capture = cv2.VideoCapture(source)
        sourceFPS = capture.get(cv2.CAP_PROP_FPS)
        print(f"Source Framerate = {sourceFPS}")
        sleepTime = 1/sourceFPS

        if not capture.isOpened():
            print("Camera Unavailable.")
            return

        print(f"Broadcaster streaming camera to {multicast_ip}:{multicast_port}")

        while True:
            frameOK, frame = capture.read()
            encodeOK, encodedFrame = cv2.imencode(".jpg", frame)
            data = encodedFrame.tobytes()

            total_chunks = len(data) // CHUNKSIZE + (1 if len(data) % CHUNKSIZE > 0 else 0)
            for i in range(total_chunks):
                start_idx = i * CHUNKSIZE
                end_idx = (i + 1) * CHUNKSIZE
                chunk = data[start_idx:end_idx]

                header = struct.pack('!II', i, total_chunks)
                packet = header + chunk

                # Send the chunk to the multicast group
                broadcaster_socket.sendto(packet, (multicast_ip, multicast_port))

            # Do I need a sleep here to match fps?
            time.sleep(sleepTime)
    
        print("Broadcast Ended")
        capture.release()
        broadcaster_socket.close()

    def register_broadcast(self, source=0, multicast_port=5000, multicast_ip='224.1.1.1'):
        thread = threading.Thread(target=self.broadcast_udp_multicast, args=(source, multicast_port, multicast_ip))
        thread.start()
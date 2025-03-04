import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import broadcaster_udp as bc
from consumer_udp import Consumer
from display_consumer import DisplayConsumer
from scale_consumer import ScaleConsumer
from detection_consumer import DetectionConsumer

def main():
    videoSource = "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4"

    broadcast = bc.Broadcaster()
    broadcast.register_broadcast()
    broadcast.register_broadcast("C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4", 5001)

    displayCamera = Consumer("Camera", DisplayConsumer())
    displayCamera.display_fps()
    displayCameraProc = displayCamera.start()

    downsample = Consumer("Downsample", ScaleConsumer(0.2))
    downsample.display_fps()
    downsampleProc = downsample.start()

    detect = Consumer("Detect", DetectionConsumer())
    detect.display_fps()
    detectProc = detect.start()

    displayVideo = Consumer("Video", DisplayConsumer(), 5001)
    displayVideo.display_fps()
    displayVideoProc = displayVideo.start()

    displayCameraProc.join()
    downsampleProc.join()
    detectProc.join()
    displayVideoProc.join()

    print("All Processes joined")


if __name__ == "__main__":
    main()
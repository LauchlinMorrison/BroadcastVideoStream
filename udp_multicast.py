import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import broadcaster_udp as bc
import consumer_udp as csmr
import scale_consumer as down
import detection_consumer as det

def main():
    videoSource = "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4"

    broadcast = bc.Broadcaster()
    broadcast.register_broadcast()
    broadcast.register_broadcast("C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4", 5001)

    displayCamera = csmr.Consumer("Camera")
    displayCamera.display_fps()
    displayCameraProc = displayCamera.start()

    downsample = down.ScaleConsumer("Downsample", 0.2)
    downsample.display_fps()
    downsampleProc = downsample.start()

    detect = det.DetectionConsumer("Detect")
    detect.display_fps()
    detectProc = detect.start()

    displayVideo = csmr.Consumer("Video", 5001)
    displayVideo.display_fps()
    displayVideoProc = displayVideo.start()

    displayCameraProc.join()
    downsampleProc.join()
    detectProc.join()
    displayVideoProc.join()

    print("All Processes joined")


if __name__ == "__main__":
    main()
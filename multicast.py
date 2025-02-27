import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import multiprocessing
import broadcaster as bc
import consumer as csmr
import downsample_consumer as down
import detection_consumer as det

def main():
    videoSource = "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4"

    broadcast = bc.Broadcaster()
    broadcast.register_broadcast()
    broadcast.register_broadcast("C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4", 5001)

    displayCamera = csmr.Consumer("Camera")
    displayCamera.display_fps()
    displayCameraProc = displayCamera.start()

    downsample = down.DownsampleConsumer("Downsample", 0.2)
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

    # consumer = multiprocessing.Process(target=csmr.display_multicast_udp)
    # consumer.start()
    # consumer2 = multiprocessing.Process(target=csmr.display_multicast_udp, args=("Display 2",))
    # consumer2.start()

    # videoStream = multiprocessing.Process(target=bc.broadcast_udp_multicast, args=(videoSource, "0.0.0.0", 5001, "224.1.1.1"))
    # videoStream.start()

    # consumer3 = multiprocessing.Process(target=csmr.display_multicast_udp, args=("Video Display", "0.0.0.0", 5001, "224.1.1.1"))
    # consumer3.start()
    # consumer4 = multiprocessing.Process(target=csmr.display_multicast_udp, args=("Video Display2", "0.0.0.0", 5001, "224.1.1.1"))
    # consumer4.start()


if __name__ == "__main__":
    main()
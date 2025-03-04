import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import broadcaster_mpq
from consumer_mpq import Consumer
from display_consumer import DisplayConsumer
from scale_consumer import ScaleConsumer
from detection_consumer import DetectionConsumer
from merge_consumer import MergeConsumer

def main():
    #source = "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4"
    consumerProcesses = []
    broadcasts = []

    broadcast = broadcaster_mpq.Broadcast("camera")
    broadcast2 = broadcaster_mpq.Broadcast("video", "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4")
    broadcasts.append(broadcast.start())
    broadcasts.append(broadcast2.start())

    display = Consumer("Display", DisplayConsumer())
    merge = Consumer("Merge", MergeConsumer())
    scale = Consumer("Downsample", ScaleConsumer(0.3))
    detect = Consumer("Detect", DetectionConsumer())

    display.subscribe(broadcast)
    merge.subscribe(broadcast)
    merge.subscribe(broadcast2)
    scale.subscribe(broadcast)
    detect.subscribe(broadcast)

    consumerProcesses.append(display.start())
    consumerProcesses.append(merge.start())
    consumerProcesses.append(scale.start())
    consumerProcesses.append(detect.start())
 

    # Wait for all consumer processes to finish
    for consumer in consumerProcesses:
        consumer.join()
    print("All consumer processes rejoined")

    # for b in broadcasts:
    #     b.terminate()

if __name__ == "__main__":
    main()
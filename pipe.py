import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import broadcaster_pipe
import consumer_pipe
import scale_consumer
import detection_consumer
import merge_consumer


def main():
    #source = "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4"
    consumerProcesses = []

    broadcast = broadcaster_pipe.Broadcast("camera")
    thread = broadcast.start()
    broadcast2 = broadcaster_pipe.Broadcast("video", "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4")
    thread2 = broadcast2.start()
    
    consumer4 = consumer_pipe.Consumer("display4")
    broadcast.subscribe(consumer4)
    consumerProcesses.append(consumer4.start())

    # consumer = merge_consumer.MergeConsumer("Merge")
    # broadcast.subscribe(consumer)
    # broadcast2.subscribe(consumer)
    # consumerProcesses.append(consumer.start())

    # consumer2 = downsample_consumer.DownsampleConsumer("Downsample", 0.3)
    # broadcast.subscribe(consumer2)
    # consumerProcesses.append(consumer2.start())

    # consumer3 = detection_consumer.DetectionConsumer("display3")
    # broadcast.subscribe(consumer3)
    # consumerProcesses.append(consumer3.start())



    # Wait for all consumer processes to finish
    for consumer in consumerProcesses:
        consumer.join()
    print("All consumer processes rejoined")

    thread.join()
    thread2.join()

if __name__ == "__main__":
    main()
import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import multiprocessing
import broadcaster as bc
import consumer as csm
import display_consumer as dc
import downsample_consumer as dsc
import detection_consumer as detc


def main():
    source = 0
    #source = "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4"
    #source = "C:/Users/Lauch/Videos/2024-11-22 19-43-23.mp4"

    # Initialize shared queue.
    frame_queue = multiprocessing.Queue(maxsize=10)

    # Start the broadcast process.
    # broadcaster = multiprocessing.Process(target=bc.capture_video_process_queue, args=(source, frame_queue))
    # broadcaster.start()

    broadcaster = multiprocessing.Process(target=bc.capture_video_multicast_udp, args=(source, "0.0.0.0", 5000, 2))
    broadcaster.start()

    displayConsumer = csm.Consumer()

    # Start consumer processes
    consumers = []
    consumers.append(multiprocessing.Process(target=dc.display, args=("Display Consumer", "0.0.0.0", 5000)))
    
    #consumers.append(multiprocessing.Process(target=displayConsumer.display, args=(frame_queue, "Display Consumer")))
    #consumers.append(multiprocessing.Process(target=dsc.display, args=(frame_queue, "Downsample Consumer")))
    #consumers.append(multiprocessing.Process(target=detc.display, args=(frame_queue, "Detection Consumer")))
    [consumer.start() for consumer in consumers]

    # Wait for all consumer processes to finish
    for consumer in consumers:
        consumer.join()
    print("All consumer processes exited")

    broadcaster.terminate()
    print("Broadcaster termindated")

if __name__ == "__main__":
    main()
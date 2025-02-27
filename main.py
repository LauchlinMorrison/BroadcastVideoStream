import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
import broadcaster_mpq
import consumer_mpq
import downsample_consumer


def main():
    #source = "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4"
    #source = "C:/Users/Lauch/Videos/2024-11-22 19-43-23.mp4"

    broadcast = broadcaster_mpq.Broadcast("camera")
    broadcast2 = broadcaster_mpq.Broadcast("video", "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4")
    consumer = consumer_mpq.Consumer("display")
    consumer2 = downsample_consumer.DownsampleConsumer("Downsample", 0.3)
    consumer3 = consumer_mpq.Consumer("display3")
    consumer4 = consumer_mpq.Consumer("display4")

    consumer.subscribe(broadcast.name, broadcast.assign(consumer.name))
    consumer2.subscribe(broadcast.name, broadcast.assign(consumer2.name))
    consumer3.subscribe(broadcast.name, broadcast.assign(consumer3.name))
    consumer4.subscribe(broadcast2.name, broadcast2.assign(consumer4.name))
    

    thread = broadcast.start()
    thread2 = broadcast2.start()
    process = consumer.start()
    process2 = consumer2.start()
    process3 = consumer3.start()
    process4 = consumer4.start()

    process.join()
    process2.join()
    process3.join()
    process4.join()
    print("Rejoined")
    thread.join()
    thread2.join()



    # Start the broadcast process.
    # broadcaster = multiprocessing.Process(target=bc.capture_video_process_queue, args=(source, frame_queue))
    # broadcaster.start()

    # broadcaster = multiprocessing.Process(target=bc.capture_video_multicast_udp, args=(source, "0.0.0.0", 5000, 2))
    # broadcaster.start()

    # displayConsumer = csm.Consumer()

    # Start consumer processes
    # consumers = []
    # consumers.append(multiprocessing.Process(target=dc.display, args=("Display Consumer", "0.0.0.0", 5000)))
    
    #consumers.append(multiprocessing.Process(target=displayConsumer.display, args=(frame_queue, "Display Consumer")))
    #consumers.append(multiprocessing.Process(target=dsc.display, args=(frame_queue, "Downsample Consumer")))
    #consumers.append(multiprocessing.Process(target=detc.display, args=(frame_queue, "Detection Consumer")))
    #[consumer.start() for consumer in consumers]

    # Wait for all consumer processes to finish
    # for consumer in consumers:
    #     consumer.join()
    # print("All consumer processes exited")

    # broadcaster.terminate()
    # print("Broadcaster termindated")

if __name__ == "__main__":
    main()
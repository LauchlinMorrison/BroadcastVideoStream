import os
os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
from node import Node
from multiprocessing import Manager
from display_consumer import DisplayConsumer
from detection_consumer import DetectionConsumer
from scale_consumer import ScaleConsumer
from merge_consumer import MergeConsumer

def subscribe(manager, communication_ledger, broadcast, consumer):
    queue = manager.Queue(1)

    if broadcast.id not in communication_ledger:
        communication_ledger[broadcast.id] = {"broadcasts": {}, "consumers": {}}
    broadcast_dict = communication_ledger[broadcast.id]
    broadcast_dict["consumers"][consumer.id] = queue
    communication_ledger[broadcast.id] = broadcast_dict

    if consumer.id not in communication_ledger:
        communication_ledger[consumer.id] = {"broadcasts": {}, "consumers": {}}
    consumer_dict = communication_ledger[consumer.id]
    consumer_dict["broadcasts"][broadcast.id] = queue
    communication_ledger[consumer.id] = consumer_dict

def unsubscribe(communication_ledger, broadcast, consumer):
    if broadcast.id in communication_ledger:
        broadcast_dict = communication_ledger[broadcast.id]
        del broadcast_dict["consumers"][consumer.id]
        communication_ledger[broadcast.id] = broadcast_dict
    
    if consumer.id in communication_ledger:
        consumer_dict = communication_ledger[consumer.id]
        del consumer_dict["broadcasts"][broadcast.id]
        communication_ledger[consumer.id] = consumer_dict

def main():
    nodes = {}
    with Manager() as manager:
        communication_dictionary = manager.dict()

        # Create our nodes and start them.
        nodes["camera"] = Node("camera", communication_dictionary, 0)
        nodes["video"] = Node("video", communication_dictionary, "C:/Users/Lauch/Videos/2025-02-14 11-15-10.mp4")
        nodes["detection"] = Node("detection", communication_dictionary, None, DetectionConsumer())
        nodes["rebroadcast"] = Node("rebroadcast", communication_dictionary, "re-broadcast", DisplayConsumer())
        nodes["display"] = Node("display", communication_dictionary, None, DisplayConsumer())
        nodes["merge"] = Node("merge", communication_dictionary, None, MergeConsumer())
        nodes["scale"] = Node("scale", communication_dictionary, None, ScaleConsumer(0.3))

        for node in nodes.values():
            node.start()

        subscribe(manager, communication_dictionary, nodes["camera"], nodes["detection"])
        subscribe(manager, communication_dictionary, nodes["camera"], nodes["rebroadcast"])
        subscribe(manager, communication_dictionary, nodes["camera"], nodes["merge"])
        subscribe(manager, communication_dictionary, nodes["video"], nodes["merge"])
        subscribe(manager, communication_dictionary, nodes["video"], nodes["scale"])
        subscribe(manager, communication_dictionary, nodes["rebroadcast"], nodes["display"])

        # Await all processes to be complete
        for node in nodes.values():
            if node.consumer_logic is not None:
                node.join()
        
        for node in nodes.values():
            if node.consumer_logic is None:
                node.stop()
        
        print("Application ended")

if __name__ == "__main__":
    main()
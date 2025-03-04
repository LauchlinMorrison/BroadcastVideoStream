from abc import ABC, abstractmethod

class IConsumer(ABC):

    @abstractmethod
    def process_frame(self, frame):
        pass
    def process_frames(self, frames):
        pass
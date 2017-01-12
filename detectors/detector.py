from abc import ABCMeta, abstractmethod

class Detector:
    __metaclass__ = ABCMeta

    # Returns array of game objects
    @abstractmethod
    def run(self, image):
        return ()

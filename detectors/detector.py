from abc import ABCMeta, abstractmethod

class Detector:
    __metaclass__ = ABCMeta

    # Returns array of points from the image
    @abstractmethod
    def run(self, image):
        return ()

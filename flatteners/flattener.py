from abc import ABCMeta, abstractmethod

class Flattener:
    __metaclass__ = ABCMeta

    @abstractmethod
    def setup(self, image):
        return ()

    # Returns the contour converted to inches
    @abstractmethod
    def flatten(self, points):
        return ()

from abc import ABCMeta, abstractmethod

class Flattener:
    __metaclass__ = ABCMeta

    # Returns array of points that are translated from the image
    @abstractmethod
    def flatten(self, points):
        return ()

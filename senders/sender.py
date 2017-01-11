from abc import ABCMeta, abstractmethod

class Sender:
    __metaclass__ = ABCMeta

    # Sends the points to the client/robot
    @abstractmethod
    def send(self, type, points):
        pass

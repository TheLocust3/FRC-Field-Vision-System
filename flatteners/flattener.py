from abc import ABCMeta, abstractmethod

class Flattener:
    __metaclass__ = ABCMeta

    # Returns array of game objects that are translated from the image
    @abstractmethod
    def flatten(self, game_objects):
        return ()

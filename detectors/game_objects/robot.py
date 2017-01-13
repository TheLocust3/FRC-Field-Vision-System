from detectors.game_objects.game_object import *

class Robot(GameObject):

    # X and Y from the top left corner
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def flatten(self, flattener):
        location = flattener.flatten([self.__x, self.__y])
        self.__x = location[0]
        self.__y = location[1]

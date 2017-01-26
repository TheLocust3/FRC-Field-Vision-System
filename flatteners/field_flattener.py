import cv2

from flatteners.flattener import *

class FieldFlattener(Flattener):

    __KNOW_DISTANCE = 10 # inches
    __KNOW_WIDTH = 2 # inches

    def setup(self, image):
        pass

    def flatten(self, contour):
        # Doesn't work yet
        #y = self.__distance_to_camera(contour)
        #x = 0 # TODO: Calculate x distance
        #return [x, y]
        return contour

    def __distance_to_camera(self, contour):
        rect = cv2.minAreaRect(contour)
        return (self.__KNOW_WIDTH * self.__focal_length) / rect[1][0]

    def __compute_focal_length(self, image):
        self.__focal_length = (self.__get_width_of_marker(im) * self.__KNOW_DISTANCE) / self.__KNOW_WIDTH

    def __get_width_of_marker(self, image):
        return 0 # TODO: Implement a marker

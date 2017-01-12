import cv2

class GameObject(object):

    def __init__(self, contour):
        self.__contour = contour
        self.__evaluate_contour()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def flatten(self, flattener):
        self.__contour = flattener.flatten(self.__contour)
        self.__evaluate_contour()

    def __evaluate_contour(self):
        moment = cv2.moments(self.__contour)

        if moment["m00"] == 0:
            self.__x = 0 # TODO: Find out if there is a better way of handling 0 area contours
            self.__y = 0
            return

        self.__x = moment["m10"] / moment["m00"]
        self.__y = moment["m01"] / moment["m00"]

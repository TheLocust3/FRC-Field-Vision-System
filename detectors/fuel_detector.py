import cv2
import numpy as np

from detectors.detector import *

class FuelDetector(Detector):

    def run(self, image):
        otsu = self.__otsu_transform(image)
        new_image = cv2.bitwise_and(image, image, mask = otsu)
        image = self.__create_fuel_mask(new_image)

        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        return ()

    def __otsu_transform(self, image):
        grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresh

    def __create_fuel_mask(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([20, 0, 110])
        upper = np.array([40, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        return mask

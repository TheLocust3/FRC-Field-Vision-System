import cv2
import numpy as np

from detectors.detector import *
from detectors.game_objects.fuel import *
import image_operations

class FuelDetector(Detector):

    def run(self, image):
        otsu_thresh = image_operations.ostu_threshold(image)
        new_image = cv2.bitwise_and(image, image, mask = otsu_thresh)
        image = self.__mask_image_for_fuel(new_image)

        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        fuel = []

        for contour in contours:
            fuel.append(Fuel(contour))

        return fuel

    def __mask_image_for_fuel(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower = np.array([20, 0, 110])
        upper = np.array([40, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)

        return mask

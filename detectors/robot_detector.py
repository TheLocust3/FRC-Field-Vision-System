import cv2
import cv
import numpy as np

from detectors.detector import *
from detectors.game_objects.robot import *
import image_operations

class RobotDetector(Detector):

    MAX_Y_DIFFERENCE = 80
    MAX_X_DIFFERENCE = 50 # TODO: Make this based on a formula
    BLUE_RED_TOLERANCE = 5

    def run(self, image):
        prepped_image = self.__prepare_image(image)
        contours, hierarchy = cv2.findContours(prepped_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        grouped_contours = self.__group_similar_contours(contours)

        robots = self.__find_robots(image, grouped_contours)
        array = []
        for location in robots:
            array.append(Robot(location[1], location[0]))

        return array

    # Group contours by contours that are horizontalish and verticalish with eachother
    def __group_similar_contours(self, contours):
        grouped_contours = [] # Format: each group is an array that consists of 0 -> mid_y, 1 -> mid_x, 2 -> array of each contour
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            mid_y = y + (h / 2)
            mid_x = x + (w / 2)

            i = 0
            found = False
            for group in grouped_contours:
                if mid_y < (group[0] + self.MAX_Y_DIFFERENCE) and mid_y > (group[0] - self.MAX_Y_DIFFERENCE):
                    if mid_x < (group[1] + self.MAX_X_DIFFERENCE) and mid_x > (group[1] - self.MAX_X_DIFFERENCE):
                        found = True
                        break
                i += 1
            
            if found:
                grouped_contours[i][2].append(contour)
            else:
                grouped_contours.append([mid_y, mid_x, [contour]])

        return grouped_contours

    # Get only contours with the right color and split up long contours
    def __find_robots(self, image, grouped_contours):
        robots = []
        for group in grouped_contours:
            y, x = image_operations.get_approx_contours_location(group[2])
            color = image_operations.get_avg_contour_color(np.vstack(group[2]), image)

            if image_operations.is_redish(color, self.BLUE_RED_TOLERANCE) or image_operations.is_blueish(color, self.BLUE_RED_TOLERANCE):
                length = image_operations.get_approx_contour_width(np.vstack(group[2]))
                if length > (0.6 * y):
                    robots.append([y - (length / 2), x])
                    robots.append([y + (length / 2), x])
                else:
                    robots.append([y, x])

        return robots

    def __prepare_image(self, image):
        normalized_image = image_operations.bgr_normalize(image)

        otsu_thresh = image_operations.ostu_threshold(normalized_image)

        kernel = np.ones((1, 20), np.uint8)
        final_image = cv2.erode(otsu_thresh, kernel)
        final_image = cv2.dilate(final_image, kernel)

        return final_image

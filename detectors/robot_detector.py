import cv2
import cv
import numpy as np

from detectors.detector import *
from detectors.game_objects.robot import *

class RobotDetector(Detector):

    __MAX_Y_DIFFERENCE = 80
    __MAX_X_DIFFERENCE = 50 # TODO: Make this based on a formula

    def run(self, image):
        cut_image = image[0:300, 300:(image.shape[1] - 200)]
        
        prepped_image = self.__prepare_image(cut_image)
        contours, hierarchy = cv2.findContours(prepped_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        grouped_contours = self.__group_contours(contours)

        robots = self.__find_robots(image, grouped_contours)
        array = []
        for location in robots:
            array.append(Robot(location[1], location[0]))

        return array


    def __bgr_normalize(self, im):
        for x in range(im.shape[1]):
            for y in range(im.shape[0]):
                red_value = float(im[y][x][2])
                green_value = float(im[y][x][1])
                blue_value = float(im[y][x][0])
                sum_color = red_value + green_value + blue_value
                if sum_color == 0:
                    im[y][x] = [0, 0, 0]
                else:
                    im[y][x][2] = red_value / sum_color * 255
                    im[y][x][1] = green_value / sum_color * 255
                    im[y][x][0] = blue_value / sum_color * 255

        return im

    def __get_contour_length(self, contour):
        x, y, w, h = cv2.boundingRect(contour)
        return w

    def __get_contours_location(self, group):
        avg_y = 0
        avg_x = 0
        for contour in group:
            x, y, w, h = cv2.boundingRect(contour)
            avg_y += y
            avg_x += x

        avg_y /= len(group)
        avg_x /= len(group)

        return (avg_y, avg_x)

    def __get_avg_color(self, contour, im):
        pixels = []

        mask = np.zeros(im.shape, np.uint8)
        cv2.drawContours(mask, [contour], 0, (255, 255, 255), cv.CV_FILLED)
        pixelpoints = np.transpose(np.nonzero(mask))

        for i in xrange(0, len(pixelpoints), 10): # Skip over some pixels to hopefully make this more efficient
            color = im[pixelpoints[i][0]][pixelpoints[i][1]]
            pixels.append([color[2], color[1], color[0]]) # BGR

        blue = 0
        green = 0
        red = 0

        for color in pixels:
            blue += color[0]
            green += color[1]
            red += color[2]

        blue /= len(pixels)
        green /= len(pixels)
        red /= len(pixels)

        return (blue, green, red)

    def __is_blueish(self, color):
        if color[0] - 5 > color[1]:
            return False
        elif color[0] - 5 > color[2]:
            return False

        return True

    def __is_redish(self, color):
        if color[2] - 5 > color[1]:
            return False
        elif color[2] - 5 > color[0]:
            return False
            
        return True

    # Group contours by contours that are horizontalish and verticalish with eachother
    def __group_contours(self, contours):
        grouped_contours = [] # Format: each group is an array that consists of 0 -> mid_y, 1 -> mid_x, 2 -> array of each contour
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            mid_y = y + (h / 2)
            mid_x = x + (w / 2)

            i = 0
            found = False
            for group in grouped_contours:
                if mid_y < (group[0] + self.__MAX_Y_DIFFERENCE) and mid_y > (group[0] - self.__MAX_Y_DIFFERENCE):
                    if mid_x < (group[1] + self.__MAX_X_DIFFERENCE) and mid_x > (group[1] - self.__MAX_X_DIFFERENCE):
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
            y, x = self.__get_contours_location(group[2])
            color = self.__get_avg_color(np.vstack(group[2]), image)

            if self.__is_redish(color) or self.__is_blueish(color):
                length = self.__get_contour_length(np.vstack(group[2]))
                if length > (0.6 * y):
                    robots.append([y - (length / 2), x])
                    robots.append([y + (length / 2), x])
                else:
                    robots.append([y, x])

        return robots

    def __prepare_image(self, image):
        normalized_image = self.__bgr_normalize(image)

        grey = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = np.ones((1, 20), np.uint8)
        final_image = cv2.erode(thresh, kernel)
        final_image = cv2.dilate(final_image, kernel)

        return final_image

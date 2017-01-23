import cv2
import numpy as np

from preprocessors.preprocessor import *

class FieldPreprocessor(Preprocessor):

    def preprocess_image(self, image):
        mask = self.__mask_field(image)

        return self.__cut_field(mask)

    def __mask_field(self, image):
        mask = np.zeros(image.shape, np.uint8)
        pts = np.array([[520, 100], [image.shape[1] - 450, 100], [image.shape[1], image.shape[0] - 100], [160, image.shape[0]]])
        cv2.fillPoly(mask, [pts], 255)
        return cv2.bitwise_and(image, image, mask = cv2.inRange(mask, 1, 255))

    def __cut_field(self, image):
        return image[100:image.shape[0], 100:image.shape[1]]

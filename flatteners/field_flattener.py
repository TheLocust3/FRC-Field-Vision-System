import cv2

from flatteners.flattener import *

class FieldFlattener(Flattener):

    def setup(self, image):
        pass

    def flatten(self, points):
        return [0, 0]

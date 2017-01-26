import threading
import sys

import cv2

class Vision(threading.Thread):
    
    def __init__(self, detectors, preprocessor, flattener, sender, capture_location):
        threading.Thread.__init__(self)

        self.__detectors = detectors
        self.__preprocessor = preprocessor
        self.__flattener = flattener
        self.__sender = sender
        self.__capture = cv2.VideoCapture(capture_location)

        self.__running = False

    def run(self):
        i = 0
        self.__running = True
        while (self.__running):
            ret, im = self.__capture.read()
            
            if (i == 0):
                self.__flattener.setup(im)

            im = self.__preprocessor.preprocess_image(im)

            for detector in self.__detectors:
                all_game_object = []
                for game_object in detector.run(im):
                    game_object.flatten(self.__flattener)
                    all_game_object.append(game_object)
            i += 0

    def kill(self):
        print("Killing vision thread")
        self.__running = False
        self.__capture.release()
        cv2.destroyAllWindows()

        sys.exit(0)

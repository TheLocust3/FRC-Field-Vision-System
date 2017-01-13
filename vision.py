import cv2

class Vision:
    
    def __init__(self, detectors, preprocessor, flattener, sender, capture_location):
        self.__detectors = detectors
        self.__preprocessor = preprocessor
        self.__flattener = flattener
        self.__sender = sender
        self.__capture = cv2.VideoCapture(capture_location)

    def run(self):
        while(self.__capture.isOpened()):
            ret, im = self.__capture.read()
            im = self.__preprocessor.preprocess_image(im)

            for detector in self.__detectors:
                all_game_object = []
                for game_object in detector.run(im):
                    game_object.flatten(self.__flattener)
                    all_game_object.append(game_object)

    def shutdown(self):
        self.__capture.release()
        cv2.destroyAllWindows()

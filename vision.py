import cv2

class Vision:
    
    def __init__(self, detectors, flattener, sender, capture_location):
        self.__detectors = detectors
        self.__flattener = flattener
        self.__sender = sender
        self.__capture = cv2.VideoCapture(capture_location)

    def run(self):
        while(self.__capture.isOpened()):
            ret, im = self.__capture.read()

            for detector in self.__detectors:
                all_fuel = []
                for fuel in detector.run(im):
                    fuel.flatten(self.__flattener)
                    all_fuel.append(fuel)

                print all_fuel

    def shutdown(self):
        self.__capture.release()
        cv2.destroyAllWindows()

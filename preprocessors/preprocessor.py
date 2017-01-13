from abc import ABCMeta, abstractmethod

class Preprocessor(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def preprocess_image(self, image):
        pass
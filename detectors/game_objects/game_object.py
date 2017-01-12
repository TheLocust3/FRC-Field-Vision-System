class GameObject(object):

    def __init__(self, contour):
        self.__contour = contour
        self.__evaluate_contour()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def flatten(self, flattener):
        self.__contour = flattener.flatten(self.__contour)
        self.__evaluate_contour()

    def __evaluate_contour(self):
        self.__x = 0
        self.__y = 0

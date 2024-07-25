import numpy as np


# Shall be initialized by 2D-array, each value in which
# represents the state of one pixel:
# "0" - pixel is turned off;
# "1" - pixel is turned on.
# While being iterated returns Pixel object to calculate distance.
class PixelMatrix:

    # Each pixel size in micrometers
    PIXEL_X_SIZE = 10
    PIXEL_Y_SIZE = 10

    def __init__(self, turned_on_ndarray):
        (self.__number_of_pixels_x, self.__number_of_pixels_y) = turned_on_ndarray.shape
        self.__max_pixel_index = self.__number_of_pixels_x * self.__number_of_pixels_y
        self.__is_turned_on_iter = np.nditer(turned_on_ndarray)
        self.__pixel_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.__pixel_index < self.__max_pixel_index:
            self.__pixel_index += 1
            return Pixel(self.x_pos(), self.y_pos(), next(self.__is_turned_on_iter))
        raise StopIteration
    
    def x_pos(self):
        return self.__pixel_index % self.__number_of_pixels_x * self.PIXEL_X_SIZE
    
    def y_pos(self):
        return self.__pixel_index // self.__number_of_pixels_x * self.PIXEL_Y_SIZE
    
    # The whole pixel matrix size in micrometers

    def x_size(self):
        return self.PIXEL_X_SIZE * self.__number_of_pixels_x
    
    def y_size(self):
        return self.PIXEL_Y_SIZE * self.__number_of_pixels_y
    
    # The whole pixel matrix size in pixels

    def number_of_pixels_x(self):
        return self.__number_of_pixels_x
    
    def number_of_pixels_y(self):
        return self.__number_of_pixels_y


class Pixel:

    def __init__(self, x, y, is_turned_on):
        self.__x_pos = x
        self.__y_pos = y
        self.__is_turned_on = is_turned_on != 0

        # Shall be used to calculate
        # the distance between the pixel and given voxel coordinates (in micrometers)
        self.distance = np.vectorize(self.__distance)

    def is_turned_on(self):
        return self.__is_turned_on

    def __distance(self, x, y, z):
        return np.sqrt((self.__x_pos - x)**2 + (self.__y_pos - y)**2 + z**2)

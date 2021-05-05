#!/usr/bin/env python3
import numpy
from preprocess.entities import image


class TrueColor(image.Image):

    NAME = "True Color"

    def __init__(self, red_band, green_band, blue_band):
        self.__red_band = red_band
        self.__green_band = green_band
        self.__blue_band = blue_band

    def name(self) -> str:
        return self.NAME

    def combine(self):
        image_dimension = self.__red_band.ndarray().shape
        image = numpy.zeros((image_dimension[0],
                             image_dimension[1],
                             3), dtype=numpy.uint16)
        image[:, :, 0] = self.__red_band.ndarray()*0.75
        image[:, :, 1] = self.__green_band.ndarray()
        image[:, :, 2] = self.__blue_band.ndarray()

        return image

    def image8bit(self):
        image16bit = self.combine()
        image8bit = (image16bit/256).astype(numpy.uint8)
        return image8bit

    def read(self):
        return self.image8bit()

    def ndarray(self):
        return self.read()

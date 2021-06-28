#!/usr/bin/env python3
import numpy
from entities.image import Image


class TrueColor(Image):

    NAME = "True Color"

    def __init__(self, red_band, green_band, blue_band):
        super().__init__()

        self.__red_band = red_band
        self.__green_band = green_band
        self.__blue_band = blue_band
        self.__scene_id = self.__red_band.scene_name()

    def name(self) -> str:
        return self.NAME

    def __combine(self) -> numpy.ndarray:
        image_dimension = self.__red_band.raw_data().shape
        image = numpy.zeros((image_dimension[0],
                             image_dimension[1],
                             3), dtype=numpy.uint16)
        image[:, :, 0] = self.__red_band.raw_data()*0.75
        image[:, :, 1] = self.__green_band.raw_data()
        image[:, :, 2] = self.__blue_band.raw_data()

        return image

    def __image8bit(self) -> numpy.ndarray:
        image16bit = self.__combine()
        image8bit = (image16bit/256).astype(numpy.uint8)
        return image8bit

    def raw_data(self) -> numpy.ndarray:
        return self.__image8bit()

    def visual_data(self) -> numpy.ndarray:
        return self.__image8bit()

    def scene_name(self):
        return self.__scene_id

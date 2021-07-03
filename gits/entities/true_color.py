#!/usr/bin/env python3
import numpy
from entities.image import Image
import cv2
from utils.utils import debug_trace

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
                             3), dtype=numpy.int32)

        image = image.astype(numpy.int32)

        image[:, :, 0] = self.__red_band.raw_data().astype(numpy.int32) * 0.88
        image[:, :, 1] = self.__green_band.raw_data().astype(numpy.int32) * 0.99
        image[:, :, 2] = self.__blue_band.raw_data().astype(numpy.int32) * 0.96

        image = numpy.clip(image, 0, 0xFFFF)

        return image

    def __image8bit(self) -> numpy.ndarray:
        image16bit = self.__combine()
        image8bit = (image16bit/256).astype(numpy.uint8)

        hsv = cv2.cvtColor(image8bit, cv2.COLOR_BGR2HSV)
        hsv = hsv.astype(numpy.int16)

        hsv[..., 1] = hsv[..., 1] * 8
        hsv[..., 2] = hsv[..., 2] * 2

        hsv = numpy.clip(hsv, 0, 255)
        hsv = hsv.astype(numpy.uint8)
        image8bit = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return image8bit

    def raw_data(self) -> numpy.ndarray:
        return self.__image8bit()

    def visual_data(self) -> numpy.ndarray:
        return self.__image8bit()

    def scene_name(self):
        return self.__scene_id

    def create_band_path(self, suffix):
        return self.__red_band.create_band_path(suffix, False)

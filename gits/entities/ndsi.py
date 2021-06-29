#!/usr/bin/env python3
import numpy
import cv2
from entities.aligned.aligned_band import AlignedBand
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class NDSI(Image):

    NAME = "NDSI"
    THRESHOLD = 0.5

    VALUE_INTERVAL = (-1, 1)

    def __init__(self, green_band: AlignedBand, swir1_band: AlignedBand):
        self.__green_band = green_band
        self.__swir1_band = swir1_band

        self.__ndsi_data = None

    def __ndsi(self):
        if self.__ndsi_data is None:
            self.__ndsi_data = self.__calculate_ndsi()
        return self.__ndsi_data

    def raw_data(self) -> numpy.ndarray:
        return self.__ndsi()

    def raw_data_16bit(self) -> numpy.ndarray:
        ndsi_16bit = self.__convert_to_16bit(self.raw_data())
        return ndsi_16bit

    def visual_data(self) -> numpy.ndarray:
        self.snow_percentage()

        ndsi_all = self.raw_data()
        ndsi_snow_ice = self.__filter_only_snow_and_ice(self.raw_data())

        ndsi_all_8bit = self.__convert_to_8bit(ndsi_all)
        ndsi_snow_ice_8bit = self.__convert_to_8bit(ndsi_snow_ice)

        ndsi_colored = cv2.cvtColor(ndsi_all_8bit, cv2.COLOR_GRAY2BGR)

        red = ndsi_snow_ice_8bit
        green = ndsi_all_8bit
        blue = ndsi_snow_ice_8bit

        ndsi_colored[..., 0] = blue
        ndsi_colored[..., 1] = green
        ndsi_colored[..., 2] = red

        return ndsi_colored

    def __convert_band_to_float32(self, band: AlignedBand) -> numpy.ndarray:
        ndarray_float32 = band.raw_data().astype(numpy.float32)
        ndarray_float32 = cv2.normalize(ndarray_float32, None, 0, 1, cv2.NORM_MINMAX)
        ndarray_float32[ndarray_float32 == 0] = numpy.nan
        return ndarray_float32

    def __calculate_ndsi(self) -> numpy.ndarray:
        # ignore division by zero because image has borders with 0 values
        numpy.seterr(divide='ignore', invalid='ignore')

        float32_green_ndarray = self.__convert_band_to_float32(self.__green_band)
        float32_swir1_ndarray = self.__convert_band_to_float32(self.__swir1_band)

        numerator = numpy.subtract(float32_green_ndarray, float32_swir1_ndarray)
        denominator = numpy.add(float32_green_ndarray, float32_swir1_ndarray)
        ndsi = numpy.divide(numerator, denominator)

        logger.info("NDSI completed.")
        return ndsi

    def __filter_only_snow_and_ice(self, ndsi):
        ndsi_snow_ice = numpy.copy(ndsi)
        ndsi_snow_ice[ndsi_snow_ice < self.THRESHOLD] = NDSI.VALUE_INTERVAL[0]
        return ndsi_snow_ice

    def __convert_to_8bit(self, ndsi) -> numpy.ndarray:
        ndsi_16bit = self.__convert_to_16bit(ndsi)
        ndsi_8bit = (ndsi_16bit >> 8).astype(numpy.uint8)
        return ndsi_8bit

    def __convert_to_16bit(self, ndsi) -> numpy.ndarray:
        # because the ndsi has values in [-1, 1] after division, we need to bring them up to
        # [0, 2^16].
        ndsi = ndsi + 1
        maximum_16bit_value = 0xFFFF
        ndsi_normalized = ndsi * maximum_16bit_value/2
        ndsi_16bit = ndsi_normalized.astype(numpy.uint16)
        return ndsi_16bit

    def snow_percentage(self) -> float:
        percentage = self.__snow_ratio() * 100
        percentage = round(percentage, 4)
        logger.notice("Snow percentage: {}%".format(percentage))
        return percentage

    def __snow_ratio(self) -> float:
        total_snow_pixels = self.__total_snow_pixels()
        total_image_pixels = self.__total_image_pixels()
        ratio = total_snow_pixels / total_image_pixels
        return ratio

    def __total_snow_pixels(self) -> int:
        ndsi = self.raw_data()
        return ndsi[ndsi > self.THRESHOLD].size

    def __total_image_pixels(self) -> int:
        ndsi = self.raw_data()
        return ndsi[ndsi == ndsi].size  # Valid data pixels (excluding NaN values)

    def name(self) -> str:
        return self.NAME

    def scene_name(self):
        return self.__green_band.scene_name()

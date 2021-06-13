#!/usr/bin/env python3
import numpy
import cv2
from entities.aligned.aligned_band import AlignedBand
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class NDSI(Image):

    NAME = "NDSI"
    THRESHOLD = 0.2

    def __init__(self, green_band: AlignedBand, swir1_band: AlignedBand):
        self.__green_band = green_band
        self.__swir1_band = swir1_band

        self.__ndsi = None

    def ndarray(self) -> numpy.ndarray:
        if self.__ndsi is None:
            self.__ndsi = self.__calculate_ndsi()
            self.__ndsi = self.__filter_snow(self.__ndsi)
            self.__ndsi = self.__convert_to_16bit(self.__ndsi)
        return self.__ndsi

    def __convert_band_to_float32(self, band: AlignedBand) -> numpy.ndarray:
        ndarray_float32 = band.ndarray().astype(numpy.float32)
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

    def __filter_snow(self, ndsi) -> numpy.ndarray:
        ndsi[ndsi < self.THRESHOLD] = 0
        return ndsi

    def __convert_to_16bit(self, ndsi) -> numpy.ndarray:
        # because the ndsi has values in [-1, 1] after division, we need to bring them up to
        # [0, 2^16].
        ndsi = ndsi + 1
        maximum_16bit_value = 0xFFFF
        ndsi_normalized = ndsi * maximum_16bit_value/2
        ndsi_16bit = ndsi_normalized.astype(numpy.uint16)
        return ndsi_16bit

    def name(self) -> str:
        return self.NAME

#!/usr/bin/env python3
import numpy
from entities.aligned.aligned_band import AlignedBand
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class NDSI(Image):

    NAME = "NDSI"

    def __init__(self, green_band: AlignedBand, swir1_band: AlignedBand):
        self.__green_band = green_band
        self.__swir1_band = swir1_band

        logger.notice("NDSI created with {} and {}.".format(self.__green_band, self.__swir1_band))

    def ndarray(self) -> numpy.ndarray:
        float32_green_ndarray = self.prepare_ndarray(self.__green_band)
        float32_swir1_ndarray = self.prepare_ndarray(self.__swir1_band)

        logger.info("Green type: {}. Swir1 type: {}.".format(type(float32_green_ndarray[0][0]), type(float32_swir1_ndarray[0][0])))

        ndsi = self.calculate_ndsi(float32_green_ndarray, float32_swir1_ndarray)
        return ndsi

    def calculate_ndsi(self, green_ndarray, swir1_ndarray) -> numpy.ndarray:
        # ignore division by zero because image has borders with 0 values
        numpy.seterr(divide='ignore', invalid='ignore')

        numerator = numpy.subtract(green_ndarray, swir1_ndarray)
        denominator = numpy.add(green_ndarray, swir1_ndarray)

        ndsi = numpy.divide(numerator, denominator)
        # interpret each NaN value as 0
        ndsi[ndsi != ndsi] = -1

        ndsi_normalized = self._normalize_to_16bit(ndsi)
        ndsi_16bit = ndsi_normalized.astype(numpy.uint16)
        logger.info("Ndsi: {}.".format(type(ndsi_16bit[0][0])))
        return ndsi_16bit

    def prepare_ndarray(self, band: AlignedBand) -> numpy.ndarray:
        ndarray_float32 = band.ndarray().astype(numpy.float32)
        ndarray_float32[ndarray_float32 == 0] = numpy.nan
        return ndarray_float32

    def name(self) -> str:
        return self.NAME

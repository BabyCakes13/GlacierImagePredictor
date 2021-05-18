#!/usr/bin/env python3
import numpy
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class AlignedBand(Image):
    def __init__(self, band):
        self.__band = band

    def ndarray(self) -> numpy.ndarray:
        unaligned_image = self.__band.read()
        return self.align(unaligned_image)

    def align(self, image):
        logger.error("Here.")
        return image + 10000000

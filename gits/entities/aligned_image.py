#!/usr/bin/env python3
import numpy
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class AlignedImage(Image):
    def __init__(self, image):
        self.__image = image

    def normalise(self, image):
        pass

    def ndarray(self) -> numpy.ndarray:
        unaligned_image = self.__image.read()
        return self.align(unaligned_image)

    def align(self, image):
        logger.info("Aligning {}".format(self.__image.name()))
        return image + 10000000

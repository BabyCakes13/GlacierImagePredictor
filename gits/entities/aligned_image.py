#!/usr/bin/env python3
import numpy
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class AlignedImage(Image):
    def __init__(self, image, reference):
        self.__image = image
        self.__reference = reference

    def ndarray(self) -> numpy.ndarray:
        unaligned_image = self.__image.read()
        return self.align(unaligned_image)

    def align(self, image):
        # TODO get affine matrix and warp it
        logger.info("Aligning {}".format(self.__image.name()))
        print(self.__reference.who())
        return image * 100000

    def __match(self):
        pass

    def __affine_transform_matrix(self):
        pass

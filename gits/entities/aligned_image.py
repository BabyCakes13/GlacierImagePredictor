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
        return self.align()

    def _raw_ndarray(self) -> numpy.ndarray:
        return self.__image._raw_ndarray()

    def align(self):
        logger.info("Aligning {}".format(self.__image.name()))

        keypoints = self.__image.keypoints()
        return self._raw_ndarray() * 100000

    def __match(self):
        pass

    def __affine_transform_matrix(self):
        pass

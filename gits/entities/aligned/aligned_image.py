#!/usr/bin/env python3
import numpy
import cv2
import os
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class AlignedImage(Image):
    def __init__(self, image, reference_scene, this_scene):
        Image.__init__(self)
        # display numpy values using decimal instead of scientific notation
        numpy.set_printoptions(suppress=True, precision=5)

        self.__image = image
        self.__matches = None
        self.__aligned_ndarray = None
        self.__this_scene = this_scene
        self.__reference_scene = reference_scene

    def raw_data(self) -> numpy.ndarray:
        return self.__ndarray()

    def visual_data(self) -> numpy.ndarray:
        return self.__ndarray()

    def create_cached_path(self):
        path = self.__image.create_band_path(suffix="_ALIGNED_CACHED")
        return path

    def __ndarray(self) -> numpy.ndarray:
        if self.__aligned_ndarray is not None:
            return self.__aligned_ndarray

        path = self.create_cached_path()
        if os.path.exists(path):
            logger.notice("Read cached file: " + path)
            self.__aligned_ndarray = cv2.imread(path, cv2.IMREAD_ANYDEPTH)
        else:
            self.__align()
            self.__aligned_ndarray = self.__resize_aligned_to_reference()
            logger.notice("Write cached file: " + path)
            cv2.imwrite(path, self.__aligned_ndarray)

        return self.__aligned_ndarray

    def __align(self) -> None:
        logger.info("Aligning {}".format(self.__image.name()))

        if self.__reference_scene == self.__this_scene:
            affine_matrix = [[1, 0, 0], [0, 1, 0]]
        else:
            affine_matrix = self.__this_scene.affine_transform_matrix()
        self.__warp_affine_transform_matrix(affine_matrix)

    def __warp_affine_transform_matrix(self, affine_transformation_matrix) -> None:
        height, width = self.__image.raw_data().shape
        self.__aligned_ndarray = cv2.warpAffine(self.__image.raw_data(),
                                                affine_transformation_matrix, (width, height))

    def __resize_aligned_to_reference(self) -> numpy.ndarray:
        reference_width = self.__reference_scene.width()
        reference_height = self.__reference_scene.height()
        image_width, image_height = self.__get_width_height(self.__aligned_ndarray)

        cropped = self.__aligned_ndarray[0: reference_height, 0: reference_width]
        logger.debug("Image: height {}, width {}".format(cropped.shape[0], cropped.shape[1]))

        difference_height = max(0, reference_height - image_height)
        difference_width = max(0, reference_width - image_width)

        padded = numpy.pad(cropped,
                           ((0, difference_height), (0, difference_width)),
                           mode='constant',
                           constant_values=0)
        logger.debug("Image: height {}, width {}".format(padded.shape[0], padded.shape[1]))

        return padded

    def __get_width_height(self, ndarray) -> tuple:
        height = ndarray.shape[0]
        width = ndarray.shape[1]

        return width, height

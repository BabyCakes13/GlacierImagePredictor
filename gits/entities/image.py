#!/usr/bin/env python3
import numpy
import cv2

from utils import logging
logger = logging.getLogger(__name__)


class Image:

    BOXES = 8
    FEATURES = 5000

    def __init__(self):
        self.__keypoints = None
        self.__descriptors = None

    def ndarray(self) -> numpy.ndarray:
        pass

    def _raw_ndarray(self) -> numpy.ndarray:
        pass

    def descriptors(self):
        if self.__descriptors is None:
            self.__compute_keypoint_descriptors()
        return self.__descriptors

    def keypoints(self):
        logger.warning("This class is {}".format(self))
        if self.__keypoints is None:
            self.__compute_keypoint_descriptors()
        return self.__keypoints

    def __compute_keypoint_descriptors(self) -> None:
        orb = cv2.ORB_create(nfeatures=self.FEATURES // self.BOXES // self.BOXES,
                             scaleFactor=2, patchSize=100)
        image = self.normalize(self._raw_ndarray())
        image = self.downsample(image)

        keypoints = self.__compute_boxed_keypoint_descriptors(image, orb)
        self.__keypoints, self.__descriptors = orb.compute(image, keypoints)

    def __compute_boxed_keypoint_descriptors(self, image, orb):
        """
        Splits the image in n boxes and applies feature finding in each, so that the points are
        evenly distributed, avoiding image distortion in the case there are feature points only in
        one part of the image.
        :param image: The image which will be split.
        :param rows: Number of rows in which the image will be split
        :param columns: Number of columns in which the image will be split
        :return: The keypoints and descriptors of the whole image
        """
        keypoints = []
        for x in range(0, self.BOXES):
            for y in range(0, self.BOXES):
                x0 = x * image.shape[1] // self.BOXES
                x1 = (x + 1) * image.shape[1] // self.BOXES
                y0 = y * image.shape[0] // self.BOXES
                y1 = (y + 1) * image.shape[0] // self.BOXES

                box_image = image[y0:y1, x0:x1]
                box_keypoints = orb.detect(box_image)

                for keypoint in box_keypoints:
                    keypoint.pt = (keypoint.pt[0] + x0, keypoint.pt[1] + y0)
                    keypoints.append(keypoint)

        return keypoints

    def downsample(self, image_16bit: numpy.ndarray):
        """
        Transforms the depth of the input image to 8 bit.
        :param image_16bit:
        :return:
        """
        image_8bit = (image_16bit >> 8).astype(numpy.uint8)

        return image_8bit

    def normalize(self, image: numpy.ndarray, bits=16):
        """
        Normalizes the input image between 0 and 2^bits.
        :param image: numpy.ndarray
        :param bits: int: number of bits for each pixel
        :return:
        """
        image = cv2.normalize(image, None, 0, (1 << bits) - 1, cv2.NORM_MINMAX)
        return image

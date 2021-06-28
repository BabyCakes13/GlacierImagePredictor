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

    def raw_data(self) -> numpy.ndarray:
        pass

    def visual_data(self) -> numpy.ndarray:
        pass

    def descriptors(self) -> numpy.ndarray:
        if self.__descriptors is None:
            self.__compute_keypoint_descriptors()
        return self.__descriptors

    def keypoints(self) -> list:
        if self.__keypoints is None:
            self.__compute_keypoint_descriptors()
        return self.__keypoints

    def __compute_keypoint_descriptors(self) -> None:
        orb = cv2.ORB_create(nfeatures=self.FEATURES // self.BOXES // self.BOXES,
                             scaleFactor=2, patchSize=100)

        keypoints = self.__compute_boxed_keypoints(self._normalized_downsampled_ndarray(), orb)
        self.__keypoints, self.__descriptors = orb.compute(self._normalized_downsampled_ndarray(),
                                                           keypoints)

    def __compute_boxed_keypoints(self, image, orb) -> list:
        """
        Splits the image in n boxes and applies feature finding in each, such that the keypoints
        are evenly distributed throughout the image, avoiding warp distortion in the case there are
        feature points only in one part of the image.
        :param image: The image which will be split.
        :param rows: Number of rows in which the image will be split
        :param columns: Number of columns in which the image will be split
        :return: The keypoints found in all the boxes
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

    def _normalized_downsampled_ndarray(self) -> numpy.ndarray:
        normalized_image = self._normalize_to_16bit(self.raw_data())
        image = self.__downsample_16bit_to_8bit(normalized_image)
        return image

    def _normalize_to_16bit(self, image: numpy.ndarray) -> numpy.ndarray:
        image = cv2.normalize(image, None, 0, (1 << 16) - 1, cv2.NORM_MINMAX)
        return image

    def __downsample_16bit_to_8bit(self, image_16bit: numpy.ndarray) -> numpy.ndarray:
        image_8bit = (image_16bit >> 8).astype(numpy.uint8)
        return image_8bit

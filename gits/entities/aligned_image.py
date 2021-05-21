#!/usr/bin/env python3
import numpy
import cv2
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class AlignedImage(Image):
    MATCHES_INCLUDED_PERCENT = 0.25

    def __init__(self, image, reference):
        Image.__init__(self)
        self.__image = image
        self.__reference = reference

    def ndarray(self) -> numpy.ndarray:
        return self.align()

    def _raw_ndarray(self) -> numpy.ndarray:
        return self.__image._raw_ndarray()

    def align(self):
        logger.info("Aligning {}".format(self.__image.name()))

        matches = self.__match()
        matches_image = self.display_matched(matches)
        return matches_image

    def __match(self):
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(self.__reference.descriptors(), self.descriptors())

        return matches

    def __prune_low_score_matches(self, matches):
        matches.sort(key=lambda x: x.distance, reverse=False)
        matches_included = int(len(matches) * self.MATCHES_INCLUDED_PERCENT)
        matches_pruned = matches[:matches_included]

        return matches_pruned

    def display_matched(self, matches):
        pruned_matches_image = cv2.drawMatches(self.__reference.normalized_downsampled_ndarray(),
                                               self.__reference.keypoints(),
                                               self.__image.normalized_downsampled_ndarray(),
                                               self.__image.keypoints(),
                                               matches,
                                               None, matchColor=(0, 255, 255),
                                               singlePointColor=(100, 0, 0),
                                               flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return pruned_matches_image

    def __affine_transform_matrix(self):
        pass

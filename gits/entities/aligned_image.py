#!/usr/bin/env python3
import numpy
import cv2
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class AlignedImage(Image):
    MATCHES_INCLUDED_PERCENT = 0.25
    EUCLIDIAN_DISTANCE = 200

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

        reference_points, image_points, matches_pruned = \
            self.__prune_matches_by_distance(matches)

        matches_image = self.__draw_matches(matches_pruned)
        return matches_image

    def __match(self):
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(self.__reference.descriptors(), self.descriptors())
        matches = self.__prune_low_score_matches(matches)

        return matches

    def __prune_low_score_matches(self, matches):
        matches.sort(key=lambda x: x.distance, reverse=False)
        matches_included = int(len(matches) * self.MATCHES_INCLUDED_PERCENT)
        matches_pruned = matches[:matches_included]

        return matches_pruned

    def __prune_matches_by_distance(self, matches):
        """
        Method which prunes the feature points pairs which are not valid (too far away from each
        other in the euclidean distance. This ensures that the remaining feature points are valid
        matches and the match line as straight as possible, which would be a 1 to 1 match.

        :return: Returns the reference and current image keypoint pairs which were left after the
        pruning, as well as the pruned matches cv2 image.
        """
        matches_pruned = []
        reference_points = []
        image_points = []

        for match in matches:
            reference_point = self.__reference.keypoints()[match.queryIdx].pt
            image_point = self.__image.keypoints()[match.trainIdx].pt

            valid_euclidean_distance = self.validate_euclidean_distance(reference_point,
                                                                        image_point)
            if valid_euclidean_distance:
                reference_points.append(reference_point)
                image_points.append(image_point)
                matches_pruned.append(match)

        reference_points = numpy.array(reference_points)
        image_points = numpy.array(image_points)

        return reference_points, image_points, matches_pruned

    @staticmethod
    def validate_euclidean_distance(reference_point, image_point) -> bool:
        """
        Calculates the difference between the reference and image coordinates. If the euclidean
        difference is too big, that means that the feature points are not correctly matched.
        If correctly matched, the distance should be as small as possible, and the match should be
        a straight line. The euclidean distance comparison allows the degree of match misalignment.
        :param reference_point: A 2D point with the coordinates of a reference feature point.
        :param image_point: A 2D point with the coordinates of a image feature point.
        :return: True, if the distance is smaller than the allowed euclidean distance, False else.
        """
        x_difference = abs(reference_point[0] - image_point[0])
        y_difference = abs(reference_point[1] - image_point[1])

        if (x_difference < AlignedImage.EUCLIDIAN_DISTANCE) and \
           (y_difference < AlignedImage.EUCLIDIAN_DISTANCE):
            return True
        else:
            return False

    def __draw_matches(self, matches):
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

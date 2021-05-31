#!/usr/bin/env python3
import numpy
import math
import cv2
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class AlignedImage(Image):

    MATCHES_INCLUDED_PERCENT = 0.25
    ALLOWED_SHIFTING_DISTANCE = 200

    def __init__(self, image, reference):
        Image.__init__(self)
        # display numpy values using decimal instead of scientific notation
        numpy.set_printoptions(suppress=True, precision=5)

        self.__image = image
        self.__reference = reference
        self.__matches = None
        self.__affine_transform_matrix = None
        self.__aligned_image = None

    def ndarray(self) -> numpy.ndarray:
        self.align()
        return self.__aligned_image

    def align(self):
        logger.info("Aligning {}".format(self.__image.name()))

        self.__matches = self.__match_descriptors()
        self.__prune_low_score_matches()
        reference_points, image_points = self.__prune_matches_by_euclidean_distance()

        self.__calculate_affine_transform_matrix(image_points, reference_points)
        self.__wrap_affine_transform_matrix()

        return self.__aligned_image

    def __match_descriptors(self) -> list:
        descriptor_match = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        reference_descriptors = self.__reference.descriptors()
        image_descriptors = self.descriptors()
        matches = descriptor_match.match(reference_descriptors, image_descriptors)
        return matches

    def __prune_low_score_matches(self) -> None:
        self.__matches.sort(key=lambda x: x.distance, reverse=False)
        matches_count = len(self.__matches)
        pruned_matches_count = int(matches_count * self.MATCHES_INCLUDED_PERCENT)
        self.__matches = self.__matches[:pruned_matches_count]

    def __prune_matches_by_euclidean_distance(self) -> tuple:
        # TODO This function should not also append the reference and image points when pruning the
        # matches by distance. Another function should do this. Not sure how to better fix it
        # without duplicate code yet,
        pruned_matches = []
        reference_points = []
        image_points = []

        for match in self.__matches:
            reference_point = self.__reference.keypoints()[match.queryIdx].pt
            image_point = self.__image.keypoints()[match.trainIdx].pt

            if self.__valid_euclidean_distance(reference_point, image_point):
                reference_points.append(reference_point)
                image_points.append(image_point)
                pruned_matches.append(match)

        self.__matches = pruned_matches
        reference_points = numpy.array(reference_points)
        image_points = numpy.array(image_points)

        return reference_points, image_points

    def __valid_euclidean_distance(self, reference_point, image_point) -> bool:
        euclidean_distance = self.__euclidean_distance(reference_point, image_point)
        if self.__euclidean_distance_valid(euclidean_distance):
            return True
        else:
            return False

    @staticmethod
    def __euclidean_distance(image_point, reference_point) -> float:
        x_distance = abs(reference_point[0] - image_point[0])
        y_distance = abs(reference_point[1] - image_point[1])
        distance = math.sqrt(math.pow(x_distance, 2) + (math.pow(y_distance, 2)))
        return distance

    @staticmethod
    def __euclidean_distance_valid(euclidean_distance) -> bool:
        if euclidean_distance < AlignedImage.ALLOWED_SHIFTING_DISTANCE:
            return True
        else:
            return False

    def __calculate_affine_transform_matrix(self, image_points, reference_points) -> None:
        try:
            affine_transform_matrix, inliers = cv2.estimateAffine2D(image_points,
                                                                    reference_points,
                                                                    None,
                                                                    cv2.RANSAC)
            self.__affine_transform_matrix = affine_transform_matrix
            logger.notice("\nAffine transformation matrix\n{}".format(affine_transform_matrix))
        except Exception as e:
            logger.ERROR("Affine transformation failed.\n{}".format(e))

    def __wrap_affine_transform_matrix(self):
        height, width = self.__image.ndarray().shape
        self.__aligned_image = cv2.warpAffine(self.__image.ndarray(),
                                              self.__affine_transform_matrix, (width, height))

    def __drawn_matches_image(self):
        drawn_matches_image = cv2.drawMatches(self.__reference.normalized_downsampled_ndarray(),
                                              self.__reference.keypoints(),
                                              self.__image.normalized_downsampled_ndarray(),
                                              self.__image.keypoints(),
                                              self.__matches,
                                              None, matchColor=(0, 255, 255),
                                              singlePointColor=(100, 0, 0),
                                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        return drawn_matches_image

    def _raw_ndarray(self) -> numpy.ndarray:
        return self.__image._raw_ndarray()

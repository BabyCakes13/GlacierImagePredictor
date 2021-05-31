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

        self.__matches = None

    def ndarray(self) -> numpy.ndarray:
        return self.align()

    def _raw_ndarray(self) -> numpy.ndarray:
        return self.__image._raw_ndarray()

    def align(self):
        logger.info("Aligning {}".format(self.__image.name()))

        self.__match()
        self.__prune_low_score_matches()
        reference_points, image_points = self.__prune_matches_by_distance()

        self.__calculate_affine_transform_matrix(image_points, reference_points)

        return aligned_image

    def __match(self):
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        self.__matches = matcher.match(self.__reference.descriptors(), self.descriptors())

    def __prune_low_score_matches(self):
        self.__matches.sort(key=lambda x: x.distance, reverse=False)
        matches_included = int(len(self.__matches) * self.MATCHES_INCLUDED_PERCENT)
        self.__matches = self.__matches[:matches_included]

    def __prune_matches_by_distance(self):
        matches_pruned = []
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

    def __wrap_affine_matrix_to_image(self, affine_matrix):
        height, width = self.__image.ndarray().shape
        print("Height: {}\nWidth: {}\nAffine: {}".format(height, width, affine_matrix))
        aligned_image = cv2.warpAffine(self.__image.ndarray(), affine_matrix, (width, height))
        return aligned_image

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

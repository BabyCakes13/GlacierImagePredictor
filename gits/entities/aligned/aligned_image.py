#!/usr/bin/env python3
import numpy
import math
import cv2
from entities.image import Image
from entities.optical_flow import OpticalFlow

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
        self.__aligned_ndarray = None

    def optical_flow(self, first_image, second_image):
        optical_flow = OpticalFlow(first_image, second_image)
        optical_flow.movement()

    def ndarray(self) -> numpy.ndarray:
        self.align()
        logger.notice("Aligned: {}, {}".format(self.__image._raw_ndarray().shape[0],
                                               self.__image._raw_ndarray().shape[1]))
        logger.notice("Reference: {}, {}".format(self.__reference._raw_ndarray().shape[0],
                                                 self.__reference._raw_ndarray().shape[1]))

        padded = self.__resize_to_reference()
        self.optical_flow(padded, self.__reference._raw_ndarray())
        return padded

    def align(self) -> None:
        logger.info("Aligning {}".format(self.__image.name()))

        self.__matches = self.__match_descriptors()
        self.__prune_low_score_matches()
        reference_points, image_points = self.__prune_matches_by_euclidean_distance()

        self.__calculate_affine_transform_matrix(image_points, reference_points)
        self.__warp_affine_transform_matrix()

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
        pruned_matches = []
        reference_points = []
        image_points = []

        for match in self.__matches:
            reference_point = self.__reference.keypoints()[match.queryIdx].pt
            image_point = self.__image.keypoints()[match.trainIdx].pt

            if self.__valid_shifting_distance(reference_point, image_point):
                reference_points.append(reference_point)
                image_points.append(image_point)
                pruned_matches.append(match)

        self.__matches = pruned_matches
        reference_points = numpy.array(reference_points)
        image_points = numpy.array(image_points)

        return reference_points, image_points

    def __valid_shifting_distance(self, reference_point, image_point) -> bool:
        euclidean_distance = self.__euclidean_distance(reference_point, image_point)
        if euclidean_distance < AlignedImage.ALLOWED_SHIFTING_DISTANCE:
            return True
        else:
            return False

    @staticmethod
    def __euclidean_distance(image_point, reference_point) -> float:
        x_distance = abs(reference_point[0] - image_point[0])
        y_distance = abs(reference_point[1] - image_point[1])
        distance = math.sqrt(math.pow(x_distance, 2) + (math.pow(y_distance, 2)))
        return distance

    def __calculate_affine_transform_matrix(self, image_points, reference_points) -> None:
        if any(element is None for element in [image_points, reference_points]):
            logger.error("Affine transformation matrix could not be computed due to insufficient \
                         valid matches.")
            self.__affine_transform_matrix = None
        try:
            affine_transform_matrix, inliers = cv2.estimateAffine2D(image_points,
                                                                    reference_points,
                                                                    None,
                                                                    cv2.RANSAC)
            self.__affine_transform_matrix = affine_transform_matrix
            logger.notice("\nAffine transformation matrix\n{}".format(affine_transform_matrix))
        except Exception as e:
            logger.error("Affine transformation failed.\n{}".format(e))

    def __warp_affine_transform_matrix(self) -> None:
        height, width = self.__image.ndarray().shape
        self.__aligned_ndarray = cv2.warpAffine(self.__image.ndarray(),
                                                self.__affine_transform_matrix, (width, height))

    def __matches_from_reference_to_image(self):
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

    def __resize_to_reference(self):
        reference_width, reference_height = self.__get_width_height(self.__reference)
        image_width, image_height = self.__get_width_height(self.__image)

        cropped = self.__image._raw_ndarray()[0: reference_height, 0: reference_width]
        logger.notice("Image: height {}, width {}".format(cropped.shape[0],
                                                          cropped.shape[1]))

        difference_height = max(0, reference_height - image_height)
        difference_width = max(0, reference_width - image_width)

        padded = numpy.pad(cropped,
                           ((0, difference_height), (0, difference_width)),
                           mode='constant',
                           constant_values=0)
        logger.notice("Image: height {}, width {}".format(padded.shape[0],
                                                          padded.shape[1]))

        return padded

    def __get_width_height(self, image):
        image_ndarray = image._raw_ndarray()
        height = image_ndarray.shape[0]
        width = image_ndarray.shape[1]

        return width, height

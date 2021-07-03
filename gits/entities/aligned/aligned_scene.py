#!/usr/bin/env python3
import numpy
import cv2
import math

from entities.image import Image
from entities.interfaces.scene_interface import SceneInterface
from entities.aligned.aligned_band import AlignedBand
from entities.motion_vectors import MotionVectors, MotionVectorsArrows
from entities.ndsi import NDSI
from entities.motion_predicted_ndsi import MotionPredictedNDSI, MotionPredictedNDSIOverlay

from utils.utils import debug_trace
from utils import logging
logger = logging.getLogger(__name__)


class AlignedScene(SceneInterface):
    MATCHES_INCLUDED_PERCENT = 0.25
    ALLOWED_SHIFTING_DISTANCE = 200

    def __init__(self, scene, reference_scene, previous_scene):
        SceneInterface.__init__(self)
        self.__scene = scene
        self.__reference_scene = reference_scene

        self.__affine_transform_matrix = None
        self.__matches = None

        self._red_band = AlignedBand(scene.red_band(), reference_scene, self)
        self._green_band = AlignedBand(scene.green_band(), reference_scene, self)
        self._blue_band = AlignedBand(scene.blue_band(), reference_scene, self)
        self._nir_band = AlignedBand(scene.nir_band(), reference_scene, self)
        self._swir1_band = AlignedBand(scene.swir1_band(), reference_scene, self)

        self.__bands = [
            self._red_band,
            self._green_band,
            self._blue_band,
            self._nir_band,
            self._swir1_band,
        ]

        self.__ndsi = NDSI(self._green_band, self._swir1_band)
        self.__bands.append(self.__ndsi)

        self.__drawn_matches_image = DrawnMatchesImage(scene, reference_scene, self)
        self.__bands.append(self.__drawn_matches_image)

        if previous_scene is not None:
            self.__motion_vectors = MotionVectors(previous_scene.ndsi(), self.__ndsi)
            self.__bands.append(self.__motion_vectors)

            self.__motion_vectors_arrows = MotionVectorsArrows(self.__motion_vectors,
                                                               previous_scene.ndsi(),
                                                               self.__ndsi)
            self.__bands.append(self.__motion_vectors_arrows)

            self.__motion_predicted_ndsi = MotionPredictedNDSI(self.__motion_vectors, self.ndsi())
            self.__bands.append(self.__motion_predicted_ndsi)

            self.__motion_predicted_overlay_ndsi = \
                MotionPredictedNDSIOverlay(self.__motion_predicted_ndsi, self.ndsi())
            self.__bands.append(self.__motion_predicted_overlay_ndsi)
        else:
            self.__motion_vectors = None
            self.__motion_predicted_ndsi = None

    def clear(self):
        for b in self.__bands:
            b.clear()

    def affine_transform_matrix(self) -> numpy.ndarray:
        if self.__affine_transform_matrix is None:
            self.__calculate_affine_transform_matrix()
        return self.__affine_transform_matrix

    def __calculate_affine_transform_matrix(self) -> None:

        self.__matches = self.__match_descriptors()
        self.__prune_low_score_matches()
        reference_points, image_points = self.__prune_matches_by_euclidean_distance()

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
            logger.notice("Affine transformation matrix for scene {} with reference {}\n{}"
                          .format(self.__scene, self.__reference_scene, affine_transform_matrix))
        except Exception as e:
            logger.error("Affine transformation failed.\n{}".format(e))

    def __match_descriptors(self) -> list:
        descriptor_match = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        reference_descriptors = self.__reference_scene.descriptors()
        image_descriptors = self.__scene.descriptors()
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
            reference_point = self.__reference_scene.keypoints()[match.queryIdx].pt
            image_point = self.__scene.keypoints()[match.trainIdx].pt

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
        if euclidean_distance < AlignedScene.ALLOWED_SHIFTING_DISTANCE:
            return True
        else:
            return False

    @staticmethod
    def __euclidean_distance(image_point, reference_point) -> float:
        x_distance = abs(reference_point[0] - image_point[0])
        y_distance = abs(reference_point[1] - image_point[1])
        distance = math.sqrt(math.pow(x_distance, 2) + (math.pow(y_distance, 2)))
        return distance

    def scene_id(self) -> str:
        return self.__scene.scene_id()

    def scene_path(self) -> str:
        return self.__scene.scene_path()

    def bands(self) -> list:
        return self.__bands

    def thumbnail(self) -> AlignedBand:
        return self.__ndsi

    def ndsi(self) -> NDSI:
        return self.__ndsi

    def matches(self):
        if self.__matches is None:
            self.affine_transform_matrix()
        return self.__matches

    def motion_predicted_ndsi(self) -> NDSI:
        return self.__motion_predicted_ndsi

    def __str__(self):
        return "AlignedScene[{}]".format(self.scene_id().scene_id())

    def iterate_over_all(self):
        logger.notice(self.__str__)
        for b in self.__bands:
            if b.name() == "Motion Vectros":
                continue
            b.raw_data()

        # Make sure we don't fill the RAM
        self.__bands = None

        self.__ndsi = None
        self.__motion_vectors = None
        self.__motion_predicted_ndsi = None

        self._red_band = None
        self._green_band = None
        self._blue_band = None
        self._nir_band = None
        self._swir1_band = None


class DrawnMatchesImage(Image):

    NAME = "Drawn Matches"

    def __init__(self, scene, reference_scene, aligned_scene):
        self.__reference_scene = reference_scene
        self.__scene = scene
        self.__aligned_scene = aligned_scene

    def name(self):
        return self.NAME

    def scene_name(self):
        return self.__scene.scene_id().scene_id()

    def raw_data(self):
        pass

    def clear(self):
        pass

    def visual_data(self):
        return self.__matches_from_reference_to_image()

    def __matches_from_reference_to_image(self):
        reference_green_band_8bit = (self.__reference_scene.green_band().visual_data() >> 8).astype(numpy.uint8)
        green_band_8bit = (self.__scene.green_band().visual_data() >> 8).astype(numpy.uint8)

        drawn_matches_image = cv2.drawMatches(reference_green_band_8bit,
                                              self.__reference_scene.keypoints(),
                                              green_band_8bit,
                                              self.__scene.keypoints(),
                                              self.__aligned_scene.matches(),
                                              None, matchColor=(0, 255, 255),
                                              singlePointColor=(100, 0, 0),
                                              flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        return drawn_matches_image

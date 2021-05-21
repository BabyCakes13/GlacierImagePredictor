#!/usr/bin/env python3
import numpy


class Image:
    def __init__(self):
        self.__keypoints = None
        self.__descriptors = None

    def ndarray(self) -> numpy.ndarray:
        pass

    def descriptors(self):
        if self.__descriptors is None:
            self.__compute_keypoint_descriptors()
        return self.__descriptors

    def keypoints(self):
        if self.__keypoints is None:
            self.__compute_keypoint_descriptors()
        return self.__keypoints

    def __compute_keypoint_descriptors(self):
        # TODO compute in place self.__descriptors and self.__keypoints
        pass

    def __normalise(self, image):
        pass

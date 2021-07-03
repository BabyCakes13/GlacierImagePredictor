#!/usr/bin/env python3
from entities.aligned.aligned_image import AlignedImage
from entities.true_color import TrueColor


class AlignedTrueColor(AlignedImage):
    NAME = "True Color"
    def __init__(self, true_color: TrueColor, reference_scene, this_scene):
        AlignedImage.__init__(self, true_color, reference_scene, this_scene)
        self.__true_color = true_color
        self.__reference_scene = reference_scene

    def name(self):
        return self.__true_color.name()

    def scene_name(self):
        return self.__true_color.scene_name()

    def create_cached_path(self):
        path = self.__true_color.create_band_path(suffix="_TRUE_COLOR_ALIGNED_CACHED")
        return path

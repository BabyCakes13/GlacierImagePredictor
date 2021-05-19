#!/usr/bin/env python3
from entities.scene_interface import SceneInterface
from entities.aligned_band import AlignedBand
from entities.true_color import TrueColor


class AlignedScene(SceneInterface):
    def __init__(self, scene):
        SceneInterface.__init__(self)
        self.__scene = scene

        self._red_band = AlignedBand(scene.red_band())
        self._green_band = AlignedBand(scene.green_band())
        self._blue_band = AlignedBand(scene.blue_band())
        self._nir_band = AlignedBand(scene.nir_band())
        self._swir1_band = AlignedBand(scene.swir1_band())

        self._true_color = TrueColor(self._red_band, self._green_band, self._blue_band)

    def scene_id(self):
        return self.__scene.scene_id()

    def scene_path(self):
        return self.__scene.scene_path()

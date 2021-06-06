#!/usr/bin/env python3
from entities.interfaces.scene_interface import SceneInterface
from entities.aligned.aligned_band import AlignedBand
from entities.ndsi import NDSI


class AlignedScene(SceneInterface):
    def __init__(self, scene, reference_scene):
        SceneInterface.__init__(self)
        self.__scene = scene

        self._red_band = AlignedBand(scene.red_band(), reference_scene.red_band())
        self._green_band = AlignedBand(scene.green_band(), reference_scene.green_band())
        self._blue_band = AlignedBand(scene.blue_band(), reference_scene.blue_band())
        self._nir_band = AlignedBand(scene.nir_band(), reference_scene.nir_band())
        self._swir1_band = AlignedBand(scene.swir1_band(), reference_scene.swir1_band())

        self.__ndsi = NDSI(self._green_band, self._swir1_band)

    def scene_id(self):
        return self.__scene.scene_id()

    def scene_path(self):
        return self.__scene.scene_path()

    def bands(self) -> list:
        return [
            self._red_band,
            self._green_band,
            self._blue_band,
            self._nir_band,
            self._swir1_band,
            self.__ndsi
        ]

    def thumnbail(self):
        return self.__ndsi

    def __str__(self):
        return "AlignedScene[{}]".format(self.scene_id().scene_id())

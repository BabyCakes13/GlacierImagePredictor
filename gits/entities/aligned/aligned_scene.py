#!/usr/bin/env python3
from entities.interfaces.scene_interface import SceneInterface
from entities.aligned.aligned_band import AlignedBand
from entities.optical_flow import OpticalFlow
from entities.ndsi import NDSI

from utils import logging
logger = logging.getLogger(__name__)


class AlignedScene(SceneInterface):
    def __init__(self, scene, reference_scene, previous_scene):
        SceneInterface.__init__(self)
        self.__scene = scene

        self._red_band = AlignedBand(scene.red_band(), reference_scene.red_band())
        self._green_band = AlignedBand(scene.green_band(), reference_scene.green_band())
        self._blue_band = AlignedBand(scene.blue_band(), reference_scene.blue_band())
        self._nir_band = AlignedBand(scene.nir_band(), reference_scene.nir_band())
        self._swir1_band = AlignedBand(scene.swir1_band(), reference_scene.swir1_band())

        self.__bands = [
            self._red_band,
            self._green_band,
            self._blue_band,
            self._nir_band,
            self._swir1_band,
        ]

        self.__ndsi = NDSI(self._green_band, self._swir1_band)
        self.__bands.append(self.__ndsi)

        if previous_scene is not None:
            self.__optical_flow_image = OpticalFlow(self.__ndsi, previous_scene.ndsi())
            self.__bands.append(self.__optical_flow_image)
        else:
            self.__optical_flow_image = None

    def scene_id(self):
        return self.__scene.scene_id()

    def scene_path(self):
        return self.__scene.scene_path()

    def bands(self) -> list:
        return self.__bands

    def thumbnail(self):
        if self.__optical_flow_image is not None:
            return self.__optical_flow_image
        else:
            return self.__ndsi

    def ndsi(self) -> NDSI:
        return self.__ndsi

    def __str__(self):
        return "AlignedScene[{}]".format(self.scene_id().scene_id())

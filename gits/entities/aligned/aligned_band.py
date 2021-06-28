#!/usr/bin/env python3
from entities.aligned.aligned_image import AlignedImage
from entities.scene import Scene
from entities.band import Band

from utils import logging
logger = logging.getLogger(__name__)


class AlignedBand(AlignedImage):
    def __init__(self, band: Band, reference_scene: Scene, this_scene: Scene):
        AlignedImage.__init__(self, band, reference_scene, this_scene)
        self.__band = band
        self.__this_scene = this_scene

    def name(self):
        return self.__band.name()

    def band(self) -> Band:
        return self.__band

    def scene_name(self):
        return self.__band.scene_name()

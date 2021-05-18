#!/usr/bin/env python3
from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class SceneInterface:

    def red_band(self) -> Image:
        return self._red_band

    def blue_band(self) -> Image:
        return self._blue_band

    def green_band(self) -> Image:
        return self._green_band

    def nir_band(self) -> Image:
        return self._nir_band

    def swir1_band(self) -> Image:
        return self._swir1_band

    def true_color(self) -> Image:
        return self._true_color

    def thumbnail(self) -> Image:
        #  return self.true_color()
        return self.red_band()

    def bands(self) -> list:
        return [
            self._red_band,
            self._green_band,
            self._blue_band,
            self._nir_band,
            self._swir1_band,
            self._true_color
        ]

    def print_bands(self):
        logger.info("Bands for scene with id {}".format(self.__str__()))
        logger.info("{}\n{}\n{}\n{}\n{}\n".format(self._blue_band,
                                                  self._green_band,
                                                  self._red_band,
                                                  self._nir_band,
                                                  self._swir1_band))

    def __str__(self):
        return "Scene[{}]".format(self.scene_id().scene_id())

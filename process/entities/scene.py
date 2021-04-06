from process.entities.band import Band
from process.entities.scene_id import SceneID

from utils import logging
logger = logging.getLogger(__name__)


class Scene:
    def __init__(self, scene_id: SceneID, scene_path: str):
        self.__scene_id = scene_id
        self.__scene_path = scene_path

        self.__red_band = Band(scene_path, scene_id.scene_id(), 'Red')
        self.__green_band = Band(scene_path, scene_id.scene_id(), 'Green')
        self.__blue_band = Band(scene_path, scene_id.scene_id(), 'Blue')
        self.__nir_band = Band(scene_path, scene_id.scene_id(), 'NIR')
        self.__swir1_band = Band(scene_path, scene_id.scene_id(), 'SWIR1')

        logger.debug("Created {}.".format(self.__str__()))

    def red_band(self) -> Band:
        return self.__red_band

    def blue_band(self) -> Band:
        return self.__blue_band

    def green_band(self) -> Band:
        return self.__green_band

    def nir_band(self) -> Band:
        return self.__nir_band

    def swir1_band(self) -> Band:
        return self.__swir1_band

    def scene_id(self):
        return self.__scene_id

    def scene_path(self):
        return self.__scene_path

    def print_bands(self):
        logger.info("Bands for scene with id {}".format(self.__str__()))
        logger.info("{}\n{}\n{}\n{}\n{}\n".format(self.__blue_band,
                                                  self.__green_band,
                                                  self.__red_band,
                                                  self.__nir_band,
                                                  self.__swir1_band))

    def __str__(self):
        return "Scene[{}]".format(self.__scene_id.scene_id())

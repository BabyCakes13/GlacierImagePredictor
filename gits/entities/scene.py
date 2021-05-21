from entities.band import Band
from entities.scene_id import SceneID
from entities.true_color import TrueColor
from entities.scene_interface import SceneInterface

from utils import logging
logger = logging.getLogger(__name__)


class Scene(SceneInterface):
    def __init__(self, scene_id: SceneID, scene_path: str):
        self._scene_id = scene_id
        self._scene_path = scene_path

        self._red_band = Band(scene_path, scene_id.scene_id(), 'Red')
        self._green_band = Band(scene_path, scene_id.scene_id(), 'Green')
        self._blue_band = Band(scene_path, scene_id.scene_id(), 'Blue')
        self._nir_band = Band(scene_path, scene_id.scene_id(), 'NIR')
        self._swir1_band = Band(scene_path, scene_id.scene_id(), 'SWIR1')

        self._true_color = TrueColor(self._red_band, self._green_band, self._blue_band)

        logger.debug("Created {}.".format(self.__str__()))

    def true_color(self) -> TrueColor:
        return self._true_color

    def scene_id(self):
        return self._scene_id

    def scene_path(self):
        return self._scene_path

    def bands(self) -> list:
        return [
            self._red_band,
            self._green_band,
            self._blue_band,
            self._nir_band,
            self._swir1_band,
            self._true_color
        ]

    def __str__(self):
        return "Scene[{}]".format(self.scene_id().scene_id())


def find_scene_by_wgi_id(scene_id: str, scenes: list):
    for scene in scenes:
        if scene.scene_id().scene_id() == scene_id:
            return scene
    return None


def get_scene_id_list_from(scenes: list) -> list:
    return [scene.scene_id().scene_id() for scene in scenes]


def bands_names(scene) -> list:
    bands_names = []
    for band in scene.bands():
        bands_names.append(band.name())
    return bands_names

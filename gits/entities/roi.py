from entities.scene import Scene
from entities.aligned_scene import AlignedScene
from utils import logging
logger = logging.getLogger(__name__)


class RegionOfInterest:
    def __init__(self, wgi_path: int, wgi_row: int):
        """
        Constructor of the RegionOfInterest class.

        :param wgi_path: https://landsat.gsfc.nasa.gov/about/worldwide-reference-system
        :param wgi_row: https://landsat.gsfc.nasa.gov/about/worldwide-reference-system
        """
        self.__path = wgi_path
        self.__row = wgi_row

        self.__scenes = []
        self.__aligned_scenes = []
        self.__reference_scene = None

        logger.debug("Created {}.".format(self.__str__()))

    def __set_reference(self, scene):
        if self.__reference_scene is None:
            self.__reference_scene = scene

            logger.info("Updated reference scene for region of interest {} with {}."
                        .format(self.__str__(), scene))

    def path(self):
        return self.__path

    def row(self):
        return self.__row

    def add_scene(self, scene: Scene) -> None:
        self.__set_reference(scene)
        self.__scenes.append(scene)
        self.__aligned_scenes.append(AlignedScene(scene, self.__reference_scene))

    def scenes(self) -> list:
        return self.__scenes

    def aligned_scenes(self) -> list:
        return self.__aligned_scenes

    def print_scenes(self) -> None:
        for scene in self.__scenes:
            logger.info(scene)

    def str_path_row(self) -> str:
        return str(self.__path) + ":" + str(self.__row)

    def __eq__(self, other):
        if isinstance(other, RegionOfInterest):
            return self.__path == other.path() and self.__row == other.row()
        return False

    def __str__(self):
        return "RegionOfInterest[{}, {}]".format(self.__path, self.__row)


def find_roi_by_path_row(roi: RegionOfInterest, rois: list) -> RegionOfInterest:
    for r in rois:
        if roi == r.str_path_row():
            return r
    return None


def get_path_row_str_from(rois: list) -> list:
    return [roi.str_path_row() for roi in rois]
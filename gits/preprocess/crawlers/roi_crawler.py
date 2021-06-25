from preprocess.crawlers.crawler import Crawler
from entities.roi import RegionOfInterest
from entities.scene_id import SceneID
from entities.scene import Scene
from entities.glacier import Glacier

import os

from utils import logging
logger = logging.getLogger(__name__)


class RoiCrawler(Crawler):
    """
    Class which crawls through a hierarchy of directories populated with scene directories and
    creates roi and scene objects based on them.
    """

    def __init__(self, root):
        Crawler.__init__(self, root)
        self.__rois = []

        logger.debug("Created {}.".format(self.__str__()))

    def crawl(self, glacier: Glacier) -> list:
        """
        Function which crawls inside the given root directory representing a glacier, extracts and
        creates region of interests and scenes which are appended to their speficic rois.

        :param glacier: Glacier for which we search the rois and scenes.
        :return: The list of created region of interest objects.
        """
        os.chdir(self._root)
        scene_dirs = [name for name in os.listdir(".") if os.path.isdir(name)]

        allscenes = []
        for scene_dir_name in scene_dirs:
            scene = self.__create_scene_objects(scene_dir_name)
            if scene is not None:
                scene.print_bands()
                allscenes.append(scene)

        allscenes.sort(key=lambda x: x.scene_id().scene_id())

        for scene in allscenes:
            self.__create_roi_objects(scene)

        return self.__rois

    def __create_roi_objects(self, scene):
        scene_id = scene.scene_id()
        roi = RegionOfInterest(scene_id.path(), scene_id.row())
        roi = self.__add_roi(roi)
        roi.add_scene(scene)

    def __create_scene_objects(self, scene_dir_name) -> Scene:
        scene_id = SceneID(scene_dir_name)
        scene_path = os.path.join(self._root, scene_dir_name)

        try:
            scene = Scene(scene_id, scene_path)
        except FileNotFoundError as e:
            logger.warning("Scene with id {} could not be created due to missing band.\n{}"
                           .format(scene_id, e))
            return None

        return scene

    def __add_roi(self, roi: RegionOfInterest) -> RegionOfInterest:
        """
        Function to check whether a region of interest was already found, adding it if not.

        For each scene we check whether its region of interest (path and row) have been already
        found, adding it to the list of all found otherwise. At the same time, we want to add the
        scene to its region of interest. If the region of interest has already been found we will
        append the scene to the already existing one, therefore the need to return either the newly
        created roi or the alreay existing one.

        :param roi: Region of interest to be searched in the list of all  roi's and added.
        :return: A region of interest.
        """
        # TODO The logic here can be implemented better. Should not return a roi in a function
        # which is adding one to a list. Or should I?

        alread_existing_roi = self.__roi_exists(roi)
        if alread_existing_roi is None:
            self.__rois.append(roi)
            return roi
        else:
            return alread_existing_roi

    def __roi_exists(self, roi) -> RegionOfInterest:
        for r in self.__rois:
            if roi == r:
                return r
        return None

from preprocess.crawlers.crawler import Crawler
from entities.roi import RegionOfInterest
from entities.scene_id import SceneID
from entities.scene import Scene
from entities.glacier import Glacier

import os
import operator
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
            print("Scene {} month {} year {}".format(scene.scene_id().scene_id(),
                                                     scene.scene_id().month(),
                                                     scene.scene_id().year()))

        clustered_scenes = self.__cluster_scenes(allscenes)

        for scene_group in clustered_scenes:
            month_range_low = scene_group[0][0]
            month_range_high = scene_group[-1][0]
            for scene_pair in scene_group:
                scene = scene_pair[1]
                self.__create_roi_objects(scene, (month_range_low, month_range_high))

        return self.__rois

    def __cluster_scenes(self, scenes):
        monthlist = []
        for scene in scenes:
            monthlist.append((scene.scene_id().month(), scene))

        monthlist.sort(key=lambda x: x[0])
        print("Monthlist ", monthlist)

        shifted = monthlist[1:]
        shifted.append(monthlist[0])
        print("shifted   ", shifted)

        gaps = list(map(lambda x, y: x[0]-y[0], shifted, monthlist))
        for i, gap in enumerate(gaps):
            if gap < 0:
                gaps[i] = gap + 12
        print("gaps      ", gaps)

        groups = [[]]
        activegroup = 0
        for i, gap in enumerate(gaps):
            groups[activegroup].append(monthlist[i])
            if gap > 0:
                groups.append([])
                activegroup += 1

        if len(groups[-1]) == 0:
            groups.pop(-1)

        # if gaps[-1] <= 1:
        #     groups[-1].extend(groups[0])
        #     if(len(groups) > 1):
        #         groups.pop(0)

        for group in groups:
            group.sort(key=lambda x:x[1].scene_id().scene_id())

        print("grouped  ", groups)

        return groups

    def __create_roi_objects(self, scene, month_range):
        scene_id = scene.scene_id()
        roi = RegionOfInterest(scene_id.path(), scene_id.row(), month_range)
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

from process.crawlers.crawler import Crawler
from process.entities.roi import RegionOfInterest
from process.entities.scene_id import SceneID
from process.entities.scene import Scene
from process.entities.glacier import Glacier

import os


class RoiCrawler(Crawler):
    """
    Class which crawls through a hierarchy of directories populated with scene directories and
    creates roi and scene objects based on them.
    """

    def __init__(self, root):
        Crawler.__init__(self, root)
        self.__rois = []

    def crawl(self, glacier: Glacier) -> list:
        """
        Function which crawls inside the given root directory representing a glacier, extracts and
        creates region of interests and scenes which are appended to their speficic rois.

        :param glacier: Glacier for which we search the rois and scenes.
        :return: The list of created region of interest objects.
        """
        os.chdir(self._root)
        scene_dirs = [name for name in os.listdir(".") if os.path.isdir(name)]

        for scene_dir_name in scene_dirs:
            scene_id = SceneID(scene_dir_name)
            scene_path = os.path.join(self._root, scene_dir_name)
            scene = self.create_scene(scene_id, scene_path)

            roi = self.create_roi(scene_id)
            roi = self.add_roi(roi)
            roi.add_scene(scene)

        return self.__rois

    def create_roi(self, scene: SceneID) -> RegionOfInterest:
        return RegionOfInterest(scene.path(), scene.row())

    def create_scene(self, scene_id: SceneID, scene_path: str):
        return Scene(scene_id, scene_path)

    def add_roi(self, roi: RegionOfInterest) -> RegionOfInterest:
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

        alread_existing_roi = self.roi_exists(roi)
        if alread_existing_roi is None:
            self.__rois.append(roi)
            return roi
        else:
            return alread_existing_roi

    def roi_exists(self, roi) -> RegionOfInterest:
        for r in self.__rois:
            if roi == r:
                return r
        return None

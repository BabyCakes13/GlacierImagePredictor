from process.crawlers.crawler import Crawler
from process.entities.roi import RegionOfInterest
from process.entities.scene_id import SceneID

import os


class RoiCrawler(Crawler):
    def __init__(self, root):
        Crawler.__init__(self, root)
        self.__rois = []

    def crawl(self) -> None:
        os.chdir(self._root)
        scenes = [name for name in os.listdir(".") if os.path.isdir(name)]

        for scene in scenes:
            scene_id = SceneID(scene)
            roi = self.create_roi(scene_id)

            if not self.roi_appended(roi):
                self.__rois.append(roi)
                print("Added ROI {} for scene {}".format(roi, scene_id))

    def create_roi(self, scene: SceneID) -> RegionOfInterest:
        return RegionOfInterest(scene.path(), scene.row())

    def roi_appended(self, roi) -> bool:
        for r in self.__rois:
            if roi == r:
                return True
        return False

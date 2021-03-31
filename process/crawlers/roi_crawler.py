from process.crawlers.crawler import Crawler
from process.entities.roi import RegionOfInterest

import os


class RoiCrawler(Crawler):
    def __init__(self, root):
        Crawler.__init__(self, root)
        self.__rois = []

    def crawl(self) -> None:
        os.chdir(self._root)
        scenes = [name for name in os.listdir(".") if os.path.isdir(name)]

        for scene in scenes:
            print(scene)

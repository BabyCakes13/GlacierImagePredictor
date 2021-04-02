from process.crawlers.crawler import Crawler
from process.crawlers.roi_crawler import RoiCrawler
from process.entities.glacier import Glacier

import os


class GlacierCrawler(Crawler):
    GEOJSON_DIR_NAME = "geojson"

    def __init__(self, root):
        Crawler.__init__(self, root)
        self.__glaciers = []

    def crawl(self) -> None:
        os.chdir(self._root)
        wgi_ids = [name for name in os.listdir(".") if os.path.isdir(name)
                   and name != self.GEOJSON_DIR_NAME]

        for wgi_id in wgi_ids:
            glacier = self.create_glacier(wgi_id)
            self.__glaciers.append(glacier)
            self.crawl_into(glacier)

    def crawl_into(self, glacier: Glacier):
        glacier_path = os.path.join(self._root, glacier.wgi_id())

        roi_crawler = RoiCrawler(root=glacier_path)
        rois = roi_crawler.crawl(glacier)
        glacier.set_rois(rois)

        print("\nFor glacier {} we found the following rois:".format(glacier))
        for roi in glacier.rois():
            print(roi)
            roi.print_scenes()

    def create_glacier(self, wgi_id: int):
        return Glacier(wgi_id)

    def glaciers(self):
        return self.__glaciers

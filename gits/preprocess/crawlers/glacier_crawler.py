from preprocess.crawlers.crawler import Crawler
from preprocess.crawlers.roi_crawler import RoiCrawler
from entities.glacier import Glacier

import os

from utils import logging
logger = logging.getLogger(__name__)


class GlacierCrawler(Crawler):
    GEOJSON_DIR_NAME = "geojson"

    def __init__(self, root):
        Crawler.__init__(self, root)
        self.__glaciers = []

        logger.debug("Created {}.".format(self.__str__()))

    def crawl(self) -> None:
        os.chdir(self._root)
        wgi_ids = [name for name in os.listdir(".") if os.path.isdir(name)
                   and name != self.GEOJSON_DIR_NAME]

        for wgi_id in wgi_ids:
            glacier = self.__create_glacier(wgi_id)
            self.__glaciers.append(glacier)
            self.crawl_into(glacier)

    def crawl_into(self, glacier: Glacier):
        glacier_path = os.path.join(self._root, glacier.wgi_id())

        roi_crawler = RoiCrawler(root=glacier_path)
        rois = roi_crawler.crawl(glacier)
        glacier.set_rois(rois)

    def print_objects(self, glacier):
        logger.info("For glacier {}, the following regions of interest have been found:"
                    .format(glacier))
        for roi in glacier.rois():
            logger.info("For region of interest {}, the following scenes have been found:"
                        .format(str(roi)))
            roi.print_scenes()

    def __create_glacier(self, wgi_id: int):
        return Glacier(wgi_id)

    def glaciers(self):
        return self.__glaciers

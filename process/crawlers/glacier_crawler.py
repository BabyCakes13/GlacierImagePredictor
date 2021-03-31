from process.crawlers.crawler import Crawler
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

    def crawl_into(self, glacier_dir):
        os.chdir(glacier_dir)
        print(os.getcwd())

    def create_glacier(self, wgi_id: int):
        return Glacier(wgi_id)

    def glaciers(self):
        return self.__glaciers

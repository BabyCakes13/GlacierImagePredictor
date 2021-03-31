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
            self.crawl_into(glacier.wgi_id())

    def crawl_into(self, glacier_dir):
        glacier_path = os.path.join(self._root, glacier_dir)
        os.chdir(glacier_path)
        print(os.getcwd())

    def create_glacier(self, wgi_id: int):
        return Glacier(wgi_id)

    def glaciers(self):
        return self.__glaciers

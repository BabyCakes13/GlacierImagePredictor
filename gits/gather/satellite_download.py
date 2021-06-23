from satsearch import Search
from satsearch.search import SatSearchError
from satstac import ItemCollection
from satstac.thing import STACError

import concurrent.futures
import json
import os
import sys
import pathlib

from utils import logging, utils
from gather.glacier import Glacier
from gather.glacier_factory import GlacierFactory
logger = logging.getLogger(__name__)


STAC_API_URL = "https://sat-api.developmentseed.org/stac"
COLLECTION = "landsat-8-l1"

DOWNLOAD_DATA = ['MTL', 'B3', 'B6', 'B2', 'B4',  'B5', 'B4',  'thumbnail']


class Download:
    RETRY_SEARCH_COUNT = 5

    def __init__(self, glacier_CSV, cloud_cover, download_directory, threads):
        self.__threads = threads
        self.__cloud_cover = cloud_cover
        self.__download_directory = self.__setup_download_directory(download_directory)
        self.__json_download_directory = self.__setup_json_directory()
        self.__glacier_factory = GlacierFactory(glacier_CSV)

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_download_directory(self, download_directory: str) -> pathlib.Path:
        return self.__create_directory(download_directory)

    def __create_directory(self, name: str) -> pathlib.Path:
        dir = pathlib.Path(name)
        dir.mkdir(parents=True, exist_ok=True)
        return dir

    def __setup_json_directory(self) -> pathlib.Path:
        """
         Function to create the directory which holds all the json files returned after searching.
        """
        json_dir = pathlib.Path.joinpath(self.__download_directory, "geojson")
        return self.__create_directory(json_dir)

    def download_glaciers(self) -> None:
        glaciers = list(self.__glacier_factory.glaciers_map().values())

        logger.notice("Starting to search assets...")
        with concurrent.futures.ThreadPoolExecutor(self.__threads) as executor:
            for c, g in enumerate(executor.map(self.__search_glaciers, glaciers)):
                utils.progress(c + 1, len(glaciers), "Finished searching assets.")

        glaciers.sort(key=lambda x: x.number_of_scenes(), reverse=True)
        self.__pretty_print_list(glaciers)

        with concurrent.futures.ThreadPoolExecutor(self.__threads) as executor:
            for c, g in enumerate(executor.map(self.__download_assets, glaciers)):
                utils.progress(c + 1, len(glaciers), "Finished downloading assets.")

    def __search_glaciers(self, glacier: Glacier) -> None:
        items = self.__cached_search(glacier)
        if items is None:
            return

        glacier.set_number_scenes(len(items))

        logger.success("Found {} with {} scenes. "
                       .format(glacier.wgi_id(), glacier.number_of_scenes()))

    def __cached_search(self, glacier: Glacier) -> None:
        """
        Function for speeding searching.

        If the json file representing the result of the search for one glacier already exists it
        will not be created again, rather reused. In case of failures during download, there is no
        need to restart the search from 0.
        """
        glacier_json = self.__glacier_json_path(glacier)
        if os.path.exists(glacier_json):
            try:
                items = ItemCollection.open(str(glacier_json))
                items.filter("collection", ["landsat-8-l1"])
                return items
            except json.decoder.JSONDecodeError:
                return self.__search(glacier)
        else:
            return self.__search(glacier)

    def __search(self, glacier: Glacier) -> ItemCollection:
        retry_count = 0
        items = None
        while (items is None) and (retry_count < self.RETRY_SEARCH_COUNT):
            try:
                search = Search(bbox=glacier.bbox(),
                                query={'eo:cloud_cover': {'lt': self.__cloud_cover}},
                                collection=COLLECTION)
                items = search.items()
                items.filter("collection", ["landsat-8-l1"])
                items.save(self.__glacier_json_path(glacier))
                return items
            except (SatSearchError, STACError) as e:
                sys.stderr.write("Error on {} with bbox {}.\n{} ".format(str(glacier),
                                                                         glacier.bbox(),
                                                                         str(e)))
                sys.stderr.flush()
                retry_count += 1
                logger.warning("Retry {} for fetching querry {}.".format(retry_count, glacier))

    def __glacier_json_path(self, glacier: Glacier) -> pathlib.Path:
        """
        Function which holds the path to the json file created after a search querry for a glacier.
        """
        json_file_name = glacier.wgi_id() + ".json"
        json_file_path = pathlib.Path.joinpath(self.__download_directory,
                                               "geojson",
                                               json_file_name)
        logger.notice(json_file_path)
        return json_file_path

    def __pretty_print_list(self, lst: list) -> None:
        for element in lst:
            logger.info(element)

    def __download_assets(self, glacier: Glacier):
        items = self.__cached_search(glacier)
        if items is None:
            return

        logger.info("Downloading {}: {}.".format(glacier.wgi_id(), glacier.number_of_scenes()))

        glacier_download_path = self.__glacier_download_path(glacier)
        items.download_assets(DOWNLOAD_DATA,
                              path=str(pathlib.Path.joinpath(glacier_download_path,
                                                             "${id}")))

        logger.success("Finished downloading assets for glacier{}".format(glacier))

    def __glacier_download_path(self, glacier: Glacier) -> pathlib.Path:
        """
        Function for creating the download directory for one glacier.

        It will take the following form:
        ddir/WGI_ID_GLACIER_NAME/
        """
        underscored_glacier_name = glacier.name().replace(" ", "_")
        glacier_ddir_name = glacier.wgi_id() + "_" + underscored_glacier_name

        return pathlib.Path.joinpath(self.__download_directory, glacier_ddir_name)

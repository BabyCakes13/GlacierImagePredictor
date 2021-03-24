from satsearch import Search
from satsearch.search import SatSearchError
from satstac import ItemCollection
from satstac.thing import STACError

import concurrent.futures
import json
import os
import sys
import logging
import pathlib

from gather import glacier_factory
sys.path.append("..")
import utils  # noqa: E402

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

STAC_API_URL = "https://sat-api.developmentseed.org/stac"
COLLECTION = "landsat-8-l1"

DOWNLOAD_DATA = ['MTL', 'B1', 'B01', 'B02', 'B2', 'B3', 'B03', 'B4', 'B04', 'B5', 'B05', 'B6',
                 'B06', 'B7', 'B07', 'B8', 'B08', 'B9', 'B09', 'B10', 'B11', 'B12']


class Download:
    def __init__(self, glacier_CSV, cloud_cover, ddir, j):
        self.j = j
        self.cloud_cover = cloud_cover

        self.ddir = self.setup_download_directory(ddir)
        self.json_dir = self.setup_json_directory()

        print(self.ddir)
        print(self.json_dir)

        self.glacier_factory = glacier_factory.GlacierFactory(glacier_CSV)

    def download_glaciers(self):
        """Function for parallellising the download of glaciers."""
        glaciers_dict = self.glacier_factory.glaciers_dict()
        glaciers = list(glaciers_dict.values())

        with concurrent.futures.ThreadPoolExecutor(self.j) as executor:
            for c, g in enumerate(executor.map(self.search_glaciers, glaciers)):
                utils.progress(c + 1, len(glaciers), "Finished searching glaciers.")

        glaciers.sort(key=lambda x: x.number_scenes(), reverse=True)

        with concurrent.futures.ThreadPoolExecutor(self.j) as executor:
            for c, g in enumerate(executor.map(self.download_assets, glaciers)):
                utils.progress(c + 1, len(glaciers), "Finished downloading assets.")

    def search(self, glacier):
        try:
            search = Search(bbox=glacier.get_bbox(),
                            query={'eo:cloud_cover': {'lt': self.cloud_cover}},
                            collection=COLLECTION)

            items = search.items()
            # Save the returned JSON to the generated file.
            items.save(self.glacier_json_path(glacier))
            return items
        except (SatSearchError, STACError) as e:
            sys.stderr.write("Error on {} with bbox {}.\n{} ".format(str(glacier),
                                                                     glacier.get_bbox(),
                                                                     str(e)))
            sys.stderr.flush()

    def cached_search(self, glacier):
        """
        Function for speeding searching.

        If the json file representing the result of the search for one glacier already exists it
        will not be created again, rather reused. In case of failures during download, there is no
        need to restart the search from 0.
        """
        glacier_json = self.glacier_json_path(glacier)
        if os.path.exists(glacier_json):
            try:
                return ItemCollection.open(str(glacier_json))
            except json.decoder.JSONDecodeError:
                return self.search(glacier)
        else:
            return self.search(glacier)

    def search_glaciers(self, glacier):
        items = self.cached_search(glacier)
        glacier.set_number_scenes(len(items))

        print("Found {} with {} scenes. ".format(glacier.get_wgi_id(), glacier.number_scenes()))

    def download_assets(self, glacier):
        items = self.cached_search(glacier)
        print("Downloading {}: {}.".format(glacier.get_wgi_id(), glacier.number_scenes()))

        glacier_download_path = self.glacier_download_path(glacier)
        items.download_assets(DOWNLOAD_DATA,
                              path=str(pathlib.Path.joinpath(glacier_download_path,
                                                             "${date}",
                                                             "${id}")))

    def glacier_download_path(self, glacier):
        """
        Function for creating the download directory for one glacier.

        It will take the following form:
        ddir/WGI_ID_GLACIER_NAME/
        """
        underscored_glacier_name = glacier.get_name().replace(" ", "_")
        glacier_ddir_name = glacier.get_wgi_id() + "_" + underscored_glacier_name

        return pathlib.Path.joinpath(self.ddir, glacier_ddir_name)

    def glacier_json_path(self, glacier):
        json_file_name = glacier.get_wgi_id() + ".json"
        return pathlib.Path.joinpath(self.ddir, "geojson", json_file_name)

    def create_directory(self, name):
        dir = pathlib.Path(name)
        dir.mkdir(parents=True, exist_ok=True)
        return dir

    def setup_download_directory(self, ddir):
        return self.create_directory(ddir)

    def setup_json_directory(self):
        json_dir = pathlib.Path.joinpath(self.ddir, "geojson")
        return self.create_directory(json_dir)

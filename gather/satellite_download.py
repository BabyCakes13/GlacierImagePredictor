from satsearch import Search
from satsearch.search import SatSearchError
from satstac import ItemCollection
from satstac.thing import STACError

import concurrent.futures
import json
import os
import sys
import logging

from gather import glacier_factory
sys.path.append("..")
import utils  # noqa: E402

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

STAC_API_URL = "https://sat-api.developmentseed.org/stac"
COLLECTION = "landsat-8-l1"

DOWNLOAD_DATA = ['MTL', 'B1', 'B2', 'B3', 'B03', 'B04', 'B5', 'B05', 'B6', 'B06', 'B7', 'B07',
                 'B8', 'B08', 'B9', 'B09', 'B10', 'B11', 'B12']
MINIMUM_SCENE_ENTRIES = 20


class Download:
    def __init__(self, glacier_CSV, cloud_cover, ddir, j):
        self.j = j
        self.cloud_cover = cloud_cover
        self.ddir = ddir
        self.glacier_factory = glacier_factory.GlacierFactory(glacier_CSV)

    def download_glaciers(self):
        """Function for parallellising the download of glaciers."""
        glaciers_dict = self.glacier_factory.glaciers_dict()
        glaciers = glaciers_dict.values()

        with concurrent.futures.ThreadPoolExecutor(self.j) as executor:
            for c, g in enumerate(executor.map(self.downlad_glacier, glaciers)):
                utils.progress(c + 1, len(glaciers), "Finished downloading glaciers.")

    def search(self, glacier):
        try:
            search = Search(bbox=glacier.get_bbox(),
                            query={'eo:cloud_cover': {'lt': self.cloud_cover}},
                            collection=COLLECTION)

            items = search.items()
            # Save the returned JSON to the generated file.
            items.save(self.glacier_json_path(glacier))
            return items
        except SatSearchError | STACError as e:
            # TODO Handle 'dem errors.
            print("Error on {} with bbox {}.\n{}".format(str(glacier),
                                                         glacier.get_bbox(),
                                                         str(e)))

    def cached_search(self, glacier):
        glacier_json = self.glacier_json_path(glacier)
        if os.path.exists(glacier_json):
            try:
                return ItemCollection.open(glacier_json)
            except json.decoder.JSONDecodeError:
                return self.search(glacier)
        else:
            return self.search(glacier)

    def downlad_glacier(self, glacier):
        items = self.cached_search(glacier)
        glacier.set_number_scenes(len(items))

        if glacier.number_scenes() < MINIMUM_SCENE_ENTRIES:
            print("Too Low {}: {}\n".format(glacier.get_wgi_id(),
                                            glacier.number_scenes()))
            return

        print("{}: {}".format(glacier.get_wgi_id(), glacier.number_scenes()))

        # items.download_assets(DOWNLOAD_DATA,
        #                       path=self.glacier_dir_name(glacier) + '/${date}/${id}')

    def glacier_dir_name(self, glacier):
        """
        Function for creating the download directory for one glacier.

        It will take the following form:
        ddir/WGI_ID_GLACIER_NAME/
        """
        underscored_glacier_name = glacier.get_name().replace(" ", "_")

        glacier_ddir = self.ddir + glacier.get_wgi_id() + "_" + underscored_glacier_name
        return glacier_ddir
        # TODO Fix this hardcoded Linux slash. Issue  #3.

    def glacier_json_path(self, glacier):
        return self.ddir + "/" + glacier.get_wgi_id() + "_cloudcover" + str(self.cloud_cover) + ".json"

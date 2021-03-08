from satsearch import Search
from satstac import ItemCollection

import concurrent.futures

import os
import sys
import logging

from gather import glacier_factory
sys.path.append("..")
import utils  # noqa: E402

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

STAC_API_URL = "https://earth-search.aws.element84.com/v0"
COLLECTION = ["landsat-8-l1-c1"]
DOWNLOAD_DATA = ['MTL', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11']
MINIMUM_SCENE_ENTRIES = 20


class Download:
    def __init__(self, glacier_CSV, ddir, j):
        self.j = j
        self.ddir = ddir
        self.glacier_factory = glacier_factory.GlacierFactory(glacier_CSV)

    def download_glaciers(self):
        """Function for parallellising the download of glaciers."""
        glaciers = self.glacier_factory.glaciers()

        with concurrent.futures.ThreadPoolExecutor(self.j) as executor:
            for count, glacier in enumerate(executor.map(self.downlad_next_glacier, glaciers)):
                utils.progress(count + 1, len(glaciers))

        sys.stderr.write("\n")

    def downlad_next_glacier(self, glacier):
        search = Search(url=STAC_API_URL,
                        bbox=glacier.get_bbox(),
                        query={'eo:cloud_cover': {'lt': 5}},
                        collections=COLLECTION)

        self.download_glacier(search, glacier)

    def download_glacier(self, search, glacier):
        items = search.items()
        glacier_json = self.ddir + "/" + glacier.get_wgi_id() + ".json"
        items.save(glacier_json)
        ItemCollection.open(glacier_json)

        items.download_assets(DOWNLOAD_DATA,
                              filename_template=self.glacier_dir_name(glacier) + '/${date}/${id}')

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

from satsearch import Search
from satstac import ItemCollection

import concurrent.futures

import os
import sys
import logging
import csv

from gather import glacier_factory

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
                progress(count, len(glaciers))

    def downlad_next_glacier(self, glacier):
        search = Search(url=STAC_API_URL,
                        bbox=glacier.get_bbox(),
                        query={'eo:cloud_cover': {'lt': 5}},
                        collections=COLLECTION)

        self.download(search, glacier)

    def download(self, search, glacier):
        print(str(glacier))
        items = search.items()
        glacier_json = self.ddir + "/" + glacier.get_wgi_id() + ".json"

        items.save(glacier_json)
        loaded = ItemCollection.open(glacier_json)

        # print(str(len(loaded)) + " " + glacier.get_wgi_id() + " " + glacier.get_name())
        # download_dir = self.ddir + glacier.get_wgi_id()
        # filenames = items.download_assets(DOWNLOAD_DATA,  filename_template=download_dir + '/${date}/${id}')


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 7)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stderr.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stderr.flush()

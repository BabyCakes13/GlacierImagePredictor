from satsearch import Search
from satstac import ItemCollection
import os
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
    def __init__(self, csv_path):
        csv_file = open(csv_path, 'r')
        self.glaciers_dict = csv.DictReader(csv_file)
        self.glacier_factory = glacier_factory.GlacierFactory()

    # TODO Paralellize
    def download_glaciers(self):
        for gd in self.glaciers_dict:
            self.downlad_next_glacier(gd)

    def downlad_next_glacier(self, glacier_row):
        glacier = self.glacier_factory.create_glacier(glacier_row)

        search = Search(url=STAC_API_URL,
                        bbox=glacier.get_bbox(),
                        query={'eo:cloud_cover': {'lt': 5}},
                        collections=COLLECTION)
        
        self.download(search, glacier)

    def download(self, search, glacier):
        items = search.items()
        items.save("glaciers_download.json")

        loaded = ItemCollection.open("glaciers_download.json")
        # print(glacier.get_wgi_id(), " with ", len(loaded))
        print(len(loaded))

        download_dir = 'glaciers/' + glacier.get_wgi_id()
        # filenames = items.download_assets(DOWNLOAD_DATA,  filename_template=download_dir + '/${date}/${id}')

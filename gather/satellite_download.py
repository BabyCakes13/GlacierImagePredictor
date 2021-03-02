from satsearch import Search
from satstac import ItemCollection
import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

STAC_API_URL = "https://earth-search.aws.element84.com/v0"
COLLECTION = ["landsat-8-l1-c1"]
DOWNLOAD_DATA = ['MTL', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11']


class Download:
    def __init__(self, glacier_factory):
        self.glacier_factory = glacier_factory

    def download_glaciers(self):
        glacier = self.glacier_factory.get_next_glacier()
    
        while glacier is not None:
            glacier = self.glacier_factory.get_next_glacier()
            # self.downlad_next_glacier()

    def downlad_next_glacier(self):
        glacier = self.glacier_factory.get_next_glacier()
        print(glacier)

        search = Search(url=STAC_API_URL,
                        bbox=glacier.get_bbox(),
                        query={'eo:cloud_cover': {'lt': 5}},
                        collections=COLLECTION)
        print('bbox search: %s items' % search.found())
        self.download(search, glacier)

    def download(self, search, glacier):
        items = search.items(limit=10)
        print(items.summary())
        items.save("glaciers_download.json")

        loaded = ItemCollection.open("glaciers_download.json")
        print(loaded.summary(['date', 'id', 'eo:cloud_cover']))

        download_dir = 'glaciers/' + glacier.get_wgi_id()
        filenames = items.download_assets(DOWNLOAD_DATA,  filename_template=download_dir + '/${date}/${id}')
        print(filenames)

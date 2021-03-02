from satsearch import Search
from satstac import ItemCollection
import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

STAC_API_URL = "https://earth-search.aws.element84.com/v0"
COLLECTION = ["landsat-8-l1-c1"]
FILE_TEMPLATE = "test_download/${date}/${id}"


class Download:
    def __init__(self, glacier_factory):
        self.glacier_factory = glacier_factory

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
        items.save("test_download.json")

        loaded = ItemCollection.open("test_download.json")
        print(loaded.summary(['date', 'id', 'eo:cloud_cover']))

        download_dir = 'test_download/' + glacier.get_wgi_id()
        filenames = items.download_assets(['MTL', 'B3', 'B6'], filename_template=download_dir + '/${date}/${id}')
        print(filenames)

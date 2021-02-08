from satsearch import Search
from satstac import ItemCollection
import os
import logging

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)


class SIDownload:
    def __init__(self):
        pass


STAC_API_URL = "https://earth-search.aws.element84.com/v0"
COLLECTION = ["landsat-8-l1-c1"]

search = Search(url=STAC_API_URL,
                bbox=[-110, 39.5, -105, 40.5],
                query={'eo:cloud_cover': {'lt': 5}},
                collections=COLLECTION)

# need to specify URL for downloading.
print('bbox search: %s items' % search.found())

items = search.items(limit=10)
print(items.summary())
items.save("test_download.json")

loaded = ItemCollection.open("test_download.json")
print(loaded.summary(['date', 'id', 'eo:cloud_cover']))

filenames = items.download_assets(['MTL', 'B3', 'B6'], filename_template='test_download/${date}/${id}')
print(filenames)

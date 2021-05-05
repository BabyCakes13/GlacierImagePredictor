from osgeo import gdal
from matplotlib import pyplot as plt
import numpy
import ntpath

import os

from preprocess.entities import image

from utils import logging
logger = logging.getLogger(__name__)


class Band(image.Image):
    BAND_NAMING_CONVENTION = {
        '2': 'Blue',
        '3': 'Green',
        '4': 'Red',
        '5': 'NIR',
        '6': 'SWIR1'
    }

    BAND_FILE_ENDWITH = {
        'Blue': '_B2.TIF',
        'Green': '_B3.TIF',
        'Red': '_B4.TIF',
        'NIR': '_B5.TIF',
        'SWIR1': '_B6.TIF'
    }

    def __init__(self, scene_path: str, scene_id: str, name: str):
        super().__init__()

        self.__band_path = self.create_band_path(scene_path, scene_id, name)
        self.__ndarray = None

        logger.debug("Created {}.".format(self.__str__()))

    def create_band_path(self, scene_path: str, scene_id: str, name: str):
        band_path = os.path.join(scene_path, scene_id + self.BAND_FILE_ENDWITH[name])
        if os.path.exists(band_path):
            return band_path
        else:
            raise FileNotFoundError("The {} band does not exist at the following location: {}."
                                    .format(name, band_path))

    def read(self) -> numpy.ndarray:
        try:
            opened = gdal.Open(self.__band_path)
            numpy_band = opened.ReadAsArray()
            return numpy_band
        except Exception as e:
            logger.warning("Could not read the band {}\n{}".format(self.__str__(), e))
            return None

    def ndarray(self) -> numpy.ndarray:
        return self.read()

    def band_number(self):
        """
        Function which extracts the number of the band from the band filename.

        An example of the filename is the following:
        LC80552482013119LGN02_B5.TIF,
        where 5 represents the number of the band in the multispectral packet.
        """
        band_filename = ntpath.basename(self.__band_path)
        return band_filename[-5:-4]

    def name(self):
        return self.BAND_NAMING_CONVENTION[self.band_number()]

    def band_path(self):
        return self.__band_path

    def plot_band(self, ndarray) -> None:
        plt.imshow(ndarray, cmap="gray")
        plt.show()

    def __str__(self):
        return "Band[{}, {}]".format(self.name(), self.__band_path)


def find_band_by_name(band_name: str, bands: list) -> Band:
    for band in bands:
        if band.name() == band_name:
            return band
    return None


def get_name_list_from(bands: list) -> list:
    return [band.name() for band in bands]

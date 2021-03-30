from osgeo import gdal
from matplotlib import pyplot as plt
import numpy
import ntpath


class Band:
    BAND_NAMING_CONVENTION = {
        '2': 'Blue',
        '3': 'Green',
        '4': 'Red',
        '5': 'Near Infrared (NIR)',
        '6': 'SWIR 1'
    }

    def __init__(self, band_path: str):
        self.__band_path = band_path
        self.__ndarray = self.read()

    def read(self) -> numpy.ndarray:
        try:
            opened = gdal.Open(self.__band_path)
            numpy_band = opened.ReadAsArray(xoff=0,
                                            yoff=0,
                                            xsize=opened.RasterXSize,
                                            ysize=opened.RasterYSize)
            return numpy_band
        except Exception as e:
            print(e)
            return None

    def band_number(self):
        """
        Function which extracts the number of the band from the band filename.

        An example of the filename is the following:
        LC80552482013119LGN02_B5.TIF,
        where 5 represents the number of the band in the multispectral packet.
        """
        band_filename = ntpath.basename(self.__band_path)
        return band_filename[23:24]

    def band_name(self):
        return self.BAND_NAMING_CONVENTION(self.band_number())

    def plot_band(self) -> None:
        plt.imshow(self.__ndarray, cmap="gray")
        plt.show()

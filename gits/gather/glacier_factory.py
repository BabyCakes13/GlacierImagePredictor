import csv

from gather.glacier import Glacier
from utils import logging, utils
logger = logging.getLogger(__name__)


class GlacierFactory:
    def __init__(self, glaciers_CSV):
        self.__csv = open(glaciers_CSV, 'r')
        self.__csv_dict = csv.DictReader(self.__csv)
        self.__number_of_csv_entries = self.__number_of_csv_entries()
        self.__glaciers_map = {}
        logger.debug("Created {}.".format(self.__str__()))

    def __number_of_csv_entries(self) -> int:
        """
        Function to get the number of entries in the glacier CSV.

        Since DictReader is used instead of CSV, directly getting the number of entries is not
        possible without reading the entire file. Possibly might need to fix this.
        """
        glacier_entries = len(list(self.__csv_dict))
        self.__csv.seek(0)
        next(self.__csv)
        return glacier_entries

    def glaciers_map(self) -> dict:
        self.__generate_glacier_map()
        return self.__glaciers_map

    def __generate_glacier_map(self) -> None:
        """Function for converting CSV glacier data into a map of Glacier objects."""
        for c, row in enumerate(self.__csv_dict):
            glacier = self.__create_glacier(row)
            glacier_wgi_id = glacier.wgi_id()

            self.__glaciers_map[glacier_wgi_id] = glacier

            utils.progress(c + 1, self.__number_of_csv_entries,
                           "Finished converting CSV rows into glaciers.")
        logger.success("Converted CSV data into glaciers.")

    def __create_glacier(self, glacier_data: list) -> Glacier:
        glacier = Glacier(glacier_data['wgi_glacier_id'],
                          glacier_data['lat'],
                          glacier_data['lon'],
                          glacier_data['glacier_name'])

        logger.debug("Created glacier {}.".format(glacier))
        return glacier

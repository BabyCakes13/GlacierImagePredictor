import csv
import sys

from gather.glacier import Glacier
sys.path.append("..")
import utils  # noqa: E402


class GlacierFactory:
    def __init__(self, glaciers_CSV):
        self.__csv = open(glaciers_CSV, 'r')
        self.__csv_dict = csv.DictReader(self.__csv)
        self.__csv_entries = self.csv_entries()
        self.__glaciers_dict = {}

    def create_glacier(self, glacier_data):
        glacier = Glacier(glacier_data['wgi_glacier_id'],
                          glacier_data['lat'],
                          glacier_data['lon'],
                          glacier_data['glacier_name'])
        return glacier

    def generate_glacier_dict(self):
        """Function for converting CSV glacier data into a map of Glacier objects."""
        for c, row in enumerate(self.__csv_dict):
            glacier = self.create_glacier(row)
            glacier_wgi_id = glacier.wgi_id()

            self.__glaciers_dict[glacier_wgi_id] = glacier

            utils.progress(c + 1, self.__csv_entries,
                           "Finished converting CSV rows into glaciers.")

    def csv_entries(self):
        """
        Function to get the number of entries in the glacier CSV.

        Since DictReader is used instead of CSV, directly getting the number of entries is not
        possible without reading the entire file. Possibly might need to fix this.
        """
        glacier_entries = len(list(self.__csv_dict))
        self.__csv.seek(0)
        next(self.__csv)
        return glacier_entries

    def glaciers_dict(self):
        self.generate_glacier_dict()
        return self.__glaciers_dict

    def print_glaciers_dict(self):
        for wgi_id, glacier in self.__glaciers_dict.items():
            print("{}: {}".format(wgi_id, str(glacier)))

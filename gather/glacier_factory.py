import csv
import sys

from gather.glacier import Glacier
sys.path.append("..")
import utils

class GlacierFactory:
    def __init__(self, glaciers_CSV):
        self.__glaciers_CSV = open(glaciers_CSV, 'r')
        self.__glaciers_dict = csv.DictReader(self.__glaciers_CSV)
        self.__glaciers = []

    def create_glacier(self, glacier_data):
        glacier = Glacier(glacier_data['wgi_glacier_id'],
                          glacier_data['lat'],
                          glacier_data['lon'],
                          glacier_data['glacier_name'])
        return glacier

    def generate_glacier_list(self):
        """
        Function for converting CSV glacier data into a list of Glacier objects.

        Data pruning also ensures that no duplicates are allowed in the list.
        """
        for count, gd in enumerate(self.__glaciers_dict):
            glacier = self.create_glacier(gd)

            if self.already_exists(glacier) is True:
                print("Detected duplicate: " + str(glacier))
                continue

            self.__glaciers.append(glacier)
            # utils.progress(count, self.glacier_dict_entries())

    def already_exists(self, glacier):
        """
        Checker for duplicate entries in the glacier data.
        """
        for g in self.__glaciers:
            if g.get_wgi_id() == glacier.get_wgi_id():
                return True
        return False

    def glacier_dict_entries(self):
        """
        Function to get the number of entries in the glacier CSV.

        Since DictReader is used instead of CSV, directly getting the number of entries is not
        possible without reading the entire file. Possibly might need to fix this.
        """
        glacier_entries = len(list(self.__glaciers_dict))
        self.__glaciers_CSV.seek(0)
        next(self.__glaciers_CSV)
        return glacier_entries

    def glaciers(self):
        self.generate_glacier_list()
        return self.__glaciers

    def print_glaciers(self):
        for g in self.__glaciers:
            print(str(g))

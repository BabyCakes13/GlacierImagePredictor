import csv

from gather.glacier import Glacier


class GlacierFactory:
    def __init__(self, glaciers_CSV):
        csv_file = open(glaciers_CSV, 'r')
        self.__glaciers_dict = csv.DictReader(csv_file)
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
        for gd in self.__glaciers_dict:
            glacier = self.create_glacier(gd)

            if self.already_exists(glacier) is True:
                print("Detected duplicate: " + str(glacier))
                continue

            self.__glaciers.append(glacier)

    def already_exists(self, glacier):
        """
        Checker for duplicate entries in the glacier data.
        """
        for g in self.__glaciers:
            if g.get_wgi_id() == glacier.get_wgi_id():
                return True
        return False

    def glaciers(self):
        self.generate_glacier_list()
        return self.__glaciers

import csv
from gather.glacier import Glacier


class GlacierFactory:
    def __init__(self, csv_path):
        csv_file = open(csv_path, 'r')
        self.csv = csv.DictReader(csv_file)

        self.line = next(self.csv)

    def get_next_glacier(self):
        self.line = next(self.csv)

        if not self.line:
            print("No more glaciers to be read.")
            return
        else:
            return self.create_glacier()

    def create_glacier(self):
        glacier = Glacier(self.line['wgi_glacier_id'],
                          self.line['lat'],
                          self.line['lon'],
                          self.line['glacier_name'])
        return glacier

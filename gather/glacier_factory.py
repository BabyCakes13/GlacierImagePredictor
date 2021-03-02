import csv
from gather.glacier import Glacier


class GlacierFactory:
    def __init__(self, csv_path):
        csv_file = open(csv_path, 'r')
        self.csv = csv.DictReader(csv_file)

    def get_next_glacier(self) -> Glacier:
        """
        Function which returns a glacier object from a CSV line.

        A line from the provided CSV file is read and converted to a
        Glacier object.
        """
        self.line = next(self.csv, None)
        
        if self.line is not None:
            return self.create_glacier()
        else:
            return None

    def create_glacier(self):
        glacier = Glacier(self.line['wgi_glacier_id'],
                          self.line['lat'],
                          self.line['lon'],
                          self.line['glacier_name'])
        return glacier

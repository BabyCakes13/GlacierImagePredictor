from gather.glacier import Glacier


class GlacierFactory:
    def __init__(self):
        pass

    def create_glacier(self, glacier_data):
        glacier = Glacier(glacier_data['wgi_glacier_id'],
                          glacier_data['lat'],
                          glacier_data['lon'],
                          glacier_data['glacier_name'])
        return glacier


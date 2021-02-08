class Glacier:
    BBOX_SIZE = 0.00001

    def __init__(self, wgi_id, latitude, longitude, name=None):
        self.wgi_id = wgi_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def define_bounding_box(self):
        """
        Function for defining a boundig box based on the glacier's coordinates.

        The bounding box is needed for satellite image search.
        """
        min_longitude = float(self.longitude) - self.BBOX_SIZE
        min_latitude = float(self.latitude) - self.BBOX_SIZE
        max_longitude = float(self.longitude) + self.BBOX_SIZE
        max_latitude = float(self.latitude) + self.BBOX_SIZE

        self.bbox = [min_longitude,
                     min_latitude,
                     max_longitude,
                     max_latitude]

    def get_bbox(self):
        self.define_bounding_box()
        return self.bbox

    def get_wgi_id(self):
        return self.wgi_id

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def __str__(self):
        return "Glacier[{}, {}, {}, {}]".format(self.wgi_id,
                                                self.latitude,
                                                self.longitude,
                                                self.name)

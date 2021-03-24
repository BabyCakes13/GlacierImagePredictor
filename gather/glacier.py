class Glacier:
    BBOX_SIZE = 0.00001

    def __init__(self, wgi_id, latitude, longitude, name=None):
        self.wgi_id = wgi_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.__number_scenes = 0
        self.define_bounding_box()

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

    def string_bbox(self):
        string_bbox = ""
        for i, coordinate in enumerate(self.bbox):
            string_bbox += str(coordinate)
            if i != len(self.bbox) - 1:
                string_bbox += ","
        return string_bbox

    def get_bbox(self):
        return self.bbox

    def get_wgi_id(self):
        return self.wgi_id

    def get_latitude(self):
        return self.latitude

    def get_longitude(self):
        return self.longitude

    def get_name(self):
        return self.name

    def set_number_scenes(self, number_scenes):
        self.__number_scenes = number_scenes

    def number_scenes(self):
        return self.__number_scenes

    def __str__(self):
        return "Glacier[{}, {}, {}, {}, {}]".format(self.wgi_id,
                                                    self.latitude,
                                                    self.longitude,
                                                    self.__number_scenes,
                                                    self.name)

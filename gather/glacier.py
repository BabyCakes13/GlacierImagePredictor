class Glacier:
    BBOX_SIZE = 0.00001

    def __init__(self, wgi_id, latitude, longitude, name=None):
        self.__wgi_id = wgi_id
        self.__name = name
        self.__latitude = latitude
        self.__longitude = longitude
        self.__number_scenes = 0
        self.__bbox = []
        self.define_bounding_box()

    def define_bounding_box(self):
        """
        Function for defining a boundig box based on the glacier's coordinates.

        The bounding box is needed for satellite image search.
        """
        min_longitude = float(self.__longitude) - self.BBOX_SIZE
        min_latitude = float(self.__latitude) - self.BBOX_SIZE
        max_longitude = float(self.__longitude) + self.BBOX_SIZE
        max_latitude = float(self.__latitude) + self.BBOX_SIZE

        self.__bbox = [min_longitude,
                       min_latitude,
                       max_longitude,
                       max_latitude]

    def string_bbox(self):
        string_bbox = ""
        for i, coordinate in enumerate(self.__bbox):
            string_bbox += str(coordinate)
            if i != len(self.__bbox) - 1:
                string_bbox += ","
        return string_bbox

    def get_bbox(self):
        return self.__bbox

    def get_wgi_id(self):
        return self.__wgi_id

    def get_latitude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude

    def get_name(self):
        return self.__name

    def set_number_scenes(self, number_scenes):
        self.__number_scenes = number_scenes

    def number_scenes(self):
        return self.__number_scenes

    def __str__(self):
        return "Glacier[{}, {}, {}, {}, {}]".format(self.__wgi_id,
                                                    self.__latitude,
                                                    self.__longitude,
                                                    self.__number_scenes,
                                                    self.__name)

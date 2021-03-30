from stuff.roi import RegionOfInterest


class Glacier:
    BBOX_SIZE = 0.00001

    def __init__(self, wgi_id, latitude, longitude, name=None):
        """
        Constructor of the Glacier object.

        :param wgi_id: World Glacier Inventory id, which is extracted from the CSV file containing
                       entries taken from the WGI file. This is used to uniquely identify glaciers.
                       More information at https://nsidc.org/data/glacier_inventory/.
        :param latitude: The latitude of the glacier.
        :param longitude: The longitude of the glacier.
        :param name: The name of the glacier, if it exists.
        """
        self.__wgi_id = wgi_id
        self.__name = name
        self.__latitude = latitude
        self.__longitude = longitude

        self.__number_scenes = 0
        self.__bbox = self.define_bounding_box()

        # Region of Interests representing different path row pairs.
        self.__rois = []

    def define_bounding_box(self) -> list:
        """
        Function for defining a boundig box based on the glacier's coordinates.

        The bounding box is needed for satellite image search.
        More information at https://wiki.openstreetmap.org/wiki/Bounding_Box.
        """
        min_longitude = float(self.__longitude) - self.BBOX_SIZE
        min_latitude = float(self.__latitude) - self.BBOX_SIZE
        max_longitude = float(self.__longitude) + self.BBOX_SIZE
        max_latitude = float(self.__latitude) + self.BBOX_SIZE

        bbox = [min_longitude,
                min_latitude,
                max_longitude,
                max_latitude]

        return bbox

    def string_bbox(self) -> str:
        """
        Function which converts the bounding box list to a string.

        This is needed because some querries from different versions of STAC use the string format
        rather than the list format as a search query parameter.
        """
        string_bbox = ""
        for i, coordinate in enumerate(self.__bbox):
            string_bbox += str(coordinate)
            if i != len(self.__bbox) - 1:
                string_bbox += ","
        return string_bbox

    def add_roi(self, roi: RegionOfInterest) -> None:
        self.__rois.append(roi)

    def bbox(self) -> list:
        return self.__bbox

    def wgi_id(self) -> str:
        return self.__wgi_id

    def latitude(self):
        return self.__latitude

    def longitude(self):
        return self.__longitude

    def name(self) -> str:
        return self.__name

    def set_number_scenes(self, number_scenes: int):
        """
        Function which sets the number of scenes found for the glacier.

        :param number_scenes: The number of scenes the search query found for the glacier at the
                              search step.
        """
        self.__number_scenes = number_scenes

    def number_scenes(self) -> int:
        return self.__number_scenes

    def __str__(self):
        return "Glacier[{}, {}, {}, {}, {}]".format(self.__wgi_id,
                                                    self.__latitude,
                                                    self.__longitude,
                                                    self.__number_scenes,
                                                    self.__name)

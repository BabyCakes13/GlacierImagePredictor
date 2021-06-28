from utils import logging
logger = logging.getLogger(__name__)


class Glacier:
    BBOX_SIZE = 0.00001

    def __init__(self, wgi_id, latitude=None, longitude=None, name=None):
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

        self.__number_of_scenes = 0
        self.__bbox = self.__define_bounding_box()

        logger.debug("Created {}.".format(self.__str__()))

    def __define_bounding_box(self) -> list:
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

        logger.debug("Defined bounding box {}".format(bbox))

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

    def set_number_scenes(self, number_of_scenes: int) -> None:
        """
        Function which sets the number of scenes found for the glacier.

        :param number_scenes: The number of scenes the search query found for the glacier at the
                              search step.
        """
        self.__number_of_scenes = number_of_scenes
        logger.debug("Found {} scenes for glacier {}".format(number_of_scenes, self.wgi_id()))

    def number_of_scenes(self) -> int:
        return self.__number_of_scenes

    def __str__(self) -> str:
        return "Glacier[{}, {}, {}, {}, {}]".format(self.__wgi_id,
                                                    self.__latitude,
                                                    self.__longitude,
                                                    self.__number_of_scenes,
                                                    self.__name)

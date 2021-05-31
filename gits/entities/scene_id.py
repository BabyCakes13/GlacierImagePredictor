import calendar

from utils import logging
logger = logging.getLogger(__name__)


class SceneID:
    """
    Class which extracts information from a scene's identifier.

    A scene identifier has the following form:
    LXSPPPRRRYYYYDDDGSIVV, where

    L = Landsat
    X = Sensor
    S = Satellite
    PPP = WRS path
    RRR = WRS row
    YYYY = Year
    DDD = Julian day of year
    GSI = Ground station identifier
    VV = Archive version number

    More info at https://www.usgs.gov/faqs/how-can-i-tell-difference-between-landsat-collections-
    'data-and-landsat-data-i-have-downloaded?qt-news_science_products=0#qt-news_science_products
    """

    def __init__(self, scene_id: str):
        self.__scene = scene_id

        logger.debug("Created {}.".format(self.__str__()))

    def scene_id(self):
        return self.__scene

    def year(self) -> int:
        """
        Returns the year of the scene based on the character location.
        :return: int
        """
        return int(self.__scene[9:13])

    def julian_day(self) -> int:
        """
        Returns the number of days passed from the start of the year till the scene was collected.
        :return: int
        """
        return int(self.__scene[13:16])

    def month(self) -> int:
        """
        Returns the month in which the scene was collected.

        Based on the total of days passed from the start of the year.
        :return: int
        """
        year = self.year()
        days = self.julian_day()

        total_days = 0
        month = 0
        while total_days < days and month <= 12:
            month += 1
            days_in_month = calendar.monthrange(year, month)[1]
            total_days += days_in_month
        return month

    def day(self) -> int:
        """
        Returns the day of the month in which the scene was collected.

        Based on the total days passed from the start of the year.
        :return: int
        """
        year = self.year()
        days = self.julian_day()

        total_days = 0
        month = 0
        day = 0
        while total_days < days and month <= 12:
            month += 1
            days_in_month = calendar.monthrange(year, month)[1]
            day = days - total_days
            total_days += days_in_month

        return day

    def satellite(self) -> str:
        """
        Returns the initials of the satellite which collected.

        The satellite should be L from Landsat.
        :return: str
        """
        return self.__scene[0:1]

    def sensor(self) -> str:
        return self.__scene[1:2]

    def satellite_number(self) -> str:
        """
        Returns the number of the satellite which collected the scene.

        The number should be 8 in our case.
        :return: str
        """
        return self.__scene[2:3]

    def path(self) -> int:
        """
        Returns the path of the collected scene.
        :return: int
        """
        return int(self.__scene[3:6])

    def row(self) -> int:
        """
        Returns the row of the collected scene.
        :return: int
        """
        return int(self.__scene[6:9])

    def __str__(self) -> str:
        return "SceneID[{}, {}, {}, {}, {}, {}, {}, {}]".format(
            self.satellite(),
            self.sensor(),
            self.satellite_number(),
            self.path(),
            self.row(),
            self.year(),
            self.month(),
            self.day()
        )

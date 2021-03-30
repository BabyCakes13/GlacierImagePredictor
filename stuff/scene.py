from band import Band


class Scene:
    """
    Class which extracts information from a scene's name.

    A scene will have the following form:
    LXSS_LLLL_PPPRRR_YYYYMMDD_yyyymmdd_CC_TX, where

    L = Landsat
    X = Sensor (“C”=OLI/TIRS combined, “O”=OLI-only, “T”=TIRS-only, “E”=ETM+, “T”=“TM, “M”=MSS)
    SS = Satellite (”07”=Landsat 7, “08”=Landsat 8)
    LLL = Processing correction level (L1TP/L1GT/L1GS)
    PPP = WRS path
    RRR = WRS row
    YYYYMMDD = Acquisition year, month, day
    yyyymmdd - Processing year, month, day
    CC = Collection number (01, 02, …)
    TX = Collection category (“RT”=Real-Time, “T1”=Tier 1, “T2”=Tier 2.
    """

    def __init__(self, scene_name: str):
        """
        Initializes the scene object which represents the name of a scene.
        :param scene: Name of a Landsat 8 scene.
        """
        self.__scene = scene_name

        self.__red_band = None
        self.__green_band = None
        self.__blue_band = None
        self.__nir_band = None
        self.__swir1_band = None

    def set_red_band(self, band: Band):
        self.__red_band = band

    def set_blue_band(self, band: Band):
        self.__blue_band = band

    def set_green_band(self, band: Band):
        self.__green_band = band

    def set_nir_band(self, band: Band):
        self.__nir_band = band

    def set_swir1_band(self, band: Band):
        self.__swir1_band = band

    def red_band(self) -> Band:
        return self.__red_band

    def blue_band(self) -> Band:
        return self.__blue_band

    def green_band(self) -> Band:
        return self.__green_band

    def nir_band(self) -> Band:
        return self.__nir_band

    def swir1_band(self) -> Band:
        return self.__swir1_band

    def satellite(self) -> str:
        return self.split_scene()[0][0:1]

    def sensor(self) -> str:
        return self.split_scene()[0][1:2]

    def satellite_number(self) -> str:
        return self.split_scene()[0][2:4]

    def progessing_collection_level(self) -> str:
        return self.split_scene()[1][0:4]

    def wrs_path(self) -> int:
        return int(self.split_scene()[2][0:3])

    def wrs_row(self) -> int:
        return int(self.split_scene()[2][3:6])

    def year(self) -> int:
        return int(self.split_scene()[3][0:4])

    def month(self) -> int:
        return int(self.split_scene()[3][4:6])

    def day(self) -> int:
        return int(self.split_scene()[3][6:8])

    def split_scene(self):
        return self.__scene.split("_")

    def __str__(self) -> str:
        return "Scene[{}, {}, {}, {}, {}, {}, {}, {}, {}]".format(
            self.satellite(),
            self.sensor(),
            self.satellite_number(),
            self.progessing_collection_level(),
            self.wrs_path(),
            self.wrs_row(),
            self.year(),
            self.month(),
            self.day()
        )

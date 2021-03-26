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

    def __init__(self, scene):
        """
        Initializes the scene object which represents the name of a scene.
        :param scene: Name of a Landsat 8 scene.
        """
        self.__scene = scene
        self.__split_scene = scene.split("_")

    def satellite(self) -> str:
        return self.__split_scene[0][0:1]

    def sensor(self) -> str:
        return self.__split_scene[0][1:2]

    def satellite_number(self) -> str:
        return self.__split_scene[0][2:4]

    def progessing_collection_level(self) -> str:
        return self.__split_scene[1][0:4]

    def wrs_path(self) -> int:
        return int(self.__split_scene[2][0:3])

    def wrs_row(self) -> int:
        return int(self.__split_scene[2][3:6])

    def year(self) -> int:
        return int(self.__split_scene[3][0:4])

    def month(self) -> int:
        return int(self.__split_scene[3][4:6])

    def day(self) -> int:
        return int(self.__split_scene[3][6:8])

    def split_scene(self):
        return self.__split_scene

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

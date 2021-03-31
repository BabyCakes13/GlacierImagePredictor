from process.entities.band import Band


class Scene:
    def __init__(self, scene_id: str):
        self.__scene_id = scene_id
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

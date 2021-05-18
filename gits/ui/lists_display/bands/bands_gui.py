#!/usr/bin/env python3
from entities import band
from utils import logging
logger = logging.getLogger(__name__)


class BandsGui:
    def __init__(self, glaciers, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

        self.__scene = self.__default_scene(glaciers)
        self.__active_band = self.__scene.thumbnail()

    def __update_active_band(self, band) -> None:
        self.__active_band = band
        logger.info("Active band changed to {}".format(str(self.__active_band)))

    def _set_band_display(self):
        band_names = band.get_name_list_from(self.__scene.bands())
        self.__window.bands_window()._set_bands_display(band_names,
                                                        self.__band_clicked,
                                                        0, 3)
        self.__band_list_widget = self.__window.bands_window().band_list_widget()

    def __band_clicked(self, item: str):
        clicked_item = self.__band_list_widget.current_item()
        clicked_band = band.find_band_by_name(clicked_item.text(), self.__scene.bands())

        self.__update_active_band(clicked_band)
        self.__gui.main_display_gui().set_image_display(clicked_band)

    def __default_scene(self, glaciers):
        default_glacier = glaciers[0]
        default_roi = default_glacier.rois()[0]
        return default_roi.scenes()[0]

    def __active_band(self) -> band.Band:
        return self.__active_band

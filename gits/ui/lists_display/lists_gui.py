#!/usr/bin/env python3
from utils import logging

from entities import scene as sc
from entities import roi as ro
from entities import glacier as gl
from entities import band

logger = logging.getLogger(__name__)


class ListsGui:
    def __init__(self, glaciers, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

        self.__glaciers = glaciers
        self.__active_glacier = self.__glaciers[0]
        self.__active_roi = self.__active_glacier.rois()[0]
        self.__active_scene = self.__active_roi.scenes()[0]
        self.__active_band = self.__active_scene.thumbnail()

        self.__window.ndsi_plot().setGlacier(self.__active_glacier.wgi_id())

    def alignment_state_changed(self):
        self.__glacier_clicked(self.__window.lists_window().glaciers_list_widget().current_item())

    def __active_rois(self) -> list:
        return self.__active_glacier.rois()

    def __active_scenes(self) -> list:
        state_gui = self.__gui.state_gui()
        return state_gui.select_state(self.__active_roi.aligned_scenes(),
                                      self.__active_roi.scenes())

    def __active_band(self) -> band.Band:
        return self.__active_band

    def __update_active_glacier(self, glacier) -> None:
        self.__active_glacier = glacier
        self.__window.ndsi_plot().setGlacier(glacier.wgi_id())

        self.__update_rois()
        logger.info("Active glacier changed to {}".format(str(self.__active_glacier)))

    def __update_active_roi(self, roi) -> None:
        self.__active_roi = roi
        self.__update_scenes()
        logger.info("Active roi changed to {}".format(str(self.__active_roi)))

    def __update_active_scene(self, scene) -> None:
        self.__active_scene.clear()
        self.__active_scene = scene
        self.__update_bands()
        logger.info("Active scene changed to {}".format(str(self.__active_scene)))

    def __update_active_band(self, band) -> None:
        self.__active_band = band
        logger.info("Type {}".format(self.__active_scene))
        logger.info("Active band changed to {}".format(str(self.__active_band)))

    def __update_rois(self) -> None:
        self.__update_active_roi(self.__active_glacier.rois()[0])

        rois_str_format = ro.get_path_row_str_from(self.__active_rois())
        self.__window.lists_window().rois_list_widget()._update_widget_items(rois_str_format)

        self.__update_scenes()

    def __update_scenes(self) -> None:
        self.__update_active_scene(self.__active_scenes()[0])

        scenes_id_list = sc.get_scene_id_list_from(self.__active_scenes())
        self.__window.lists_window().scenes_list_widget()._update_widget_items(scenes_id_list)

        self.__update_bands()

    def __update_bands(self) -> None:
        self.__update_active_band(self.__active_scene.thumbnail())
        bands_names = sc.bands_names(self.__active_scene)
        row = self.__active_scene.bands().index(self.__active_band)
        self.__window.lists_window().bands_list_widget()._update_widget_items(bands_names, row)
        self.__gui.main_display_gui().set_image_display(self.__active_band)

        self.__window.lists_window().bands_list_widget()

    def __glacier_clicked(self, item_clicked):
        item = self.__window.lists_window().glaciers_list_widget().current_item()
        glacier = gl.find_glacier_by_wgi_id(item.text(), self.__glaciers)

        self.__update_active_glacier(glacier)

    def __roi_clicked(self, item_clicked):
        item = self.__window.lists_window().rois_list_widget().current_item()
        roi = ro.find_roi_by_path_row(item.text(), self.__active_rois())

        self.__update_active_roi(roi)
        self.__window.ndsi_plot().setROI(self.__active_roi)

    def __scene_clicked(self, item_clicked):
        item = self.__window.lists_window().scenes_list_widget().current_item()
        scene = sc.find_scene_by_wgi_id(item.text(), self.__active_scenes())
        self.__update_active_scene(scene)

    def __band_clicked(self, item_clicked: str):
        clicked_item = self.__window.lists_window().bands_list_widget().current_item()
        clicked_band = band.find_band_by_name(clicked_item.text(), self.__active_scene.bands())

        self.__update_active_band(clicked_band)
        self.__gui.main_display_gui().set_image_display(clicked_band)

        if hasattr(self.__active_band, 'snow_percentage'):
            self.__window.ndsi_plot().setROI(self.__active_roi)
            self.__window.ndsi_plot().visible(True)
        else:
            self.__window.ndsi_plot().visible(False)

    def _set_glacier_display(self):
        glaciers_str = gl.get_wgi_id_list_from(self.__glaciers)
        self.__window.lists_window()._set_default_glaciers_display(glaciers_str,
                                                                   self.__glacier_clicked)

    def _set_roi_display(self):
        rois_str = ro.get_path_row_str_from(self.__active_rois())
        self.__window.lists_window()._set_default_rois_display(rois_str,
                                                               self.__roi_clicked)

    def _set_scenes_display(self):
        scenes_str = sc.get_scene_id_list_from(self.__active_scenes())
        self.__window.lists_window()._set_default_scenes_display(scenes_str,
                                                                 self.__scene_clicked)
        self.__gui.main_display_gui().set_image_display(self.__active_band)

    def _set_band_display(self):
        band_names = band.get_name_list_from(self.__active_scene.bands())
        self.__window.lists_window()._set_default_bands_display(band_names,
                                                                self.__band_clicked)
        # TODO get rid of this hack
        self.__update_active_glacier(self.__active_glacier)

    def active_scene(self) -> sc.Scene:
        return self.__active_scene

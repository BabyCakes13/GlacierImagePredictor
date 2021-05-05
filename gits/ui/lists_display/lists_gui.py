#!/usr/bin/env python3
from utils import logging

from preprocess.entities import scene as sc
from preprocess.entities import roi as ro
from preprocess.entities import glacier as gl

logger = logging.getLogger(__name__)


class ListsGui:
    def __init__(self, glaciers, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

        self.__glaciers = glaciers
        self.__active_glacier = self.__glaciers[0]
        self.__active_roi = self.__active_glacier.rois()[0]
        self.__active_scene = self.__active_roi.scenes()[0]

        self.__active_glaciers_qlist = None
        self.__active_rois_qlist = None
        self.__active_scenes_qlist = None

    def __active_rois(self) -> list:
        return self.__active_glacier.rois()

    def __active_scenes(self) -> list:
        return self.__active_roi.scenes()

    def __update_active_glacier(self, glacier) -> None:
        self.__active_glacier = glacier
        logger.info("Active glacier changed to {}".format(str(self.__active_glacier)))

    def __update_active_roi(self, roi) -> None:
        self.__active_roi = roi
        logger.info("Active roi changed to {}".format(str(self.__active_roi)))

    def __update_active_scene(self, scene) -> None:
        self.__active_scene = scene
        self.__gui.main_display_gui().set_image_display(self.__active_scene.thumbnail_path())
        logger.info("Active scene changed to {}".format(str(self.__active_scene)))

    def __update_rois(self) -> None:
        self.__update_active_roi(self.__active_glacier.rois()[0])

        rois_str_format = ro.get_path_row_str_from(self.__active_rois())
        self.__window.lists_window().rois_list_widget()._update_widget_items(rois_str_format)

        self.__update_scenes()

    def __update_scenes(self) -> None:
        self.__update_active_scene(self.__active_roi.scenes()[0])

        scenes_id_list = sc.get_scene_id_list_from(self.__active_scenes())
        self.__window.lists_window().scenes_list_widget()._update_widget_items(scenes_id_list)

    def __glacier_clicked(self, item):
        item = self.__active_glaciers_qlist.current_item()
        glacier = gl.find_glacier_by_wgi_id(item.text(), self.__glaciers)

        self.__update_active_glacier(glacier)
        self.__update_rois()

    def __roi_clicked(self):
        item = self.__active_rois_qlist.current_item()
        roi = ro.find_roi_by_path_row(item.text(), self.__active_rois())

        self.__update_active_roi(roi)
        self.__update_scenes()

    def __scene_clicked(self, item: str):
        item = self.__active_scenes_qlist.current_item()
        scene = sc.find_scene_by_wgi_id(item.text(), self.__active_scenes())

        self.__update_active_scene(scene)

    def _set_glacier_display(self):
        glaciers_str = gl.get_wgi_id_list_from(self.__glaciers)
        self.__window.lists_window()._set_default_glaciers_display(glaciers_str,
                                                                   self.__glacier_clicked,
                                                                   0, 0)
        self.__active_glaciers_qlist = self.__window.lists_window().glaciers_list_widget()

    def _set_roi_display(self):
        rois_str = ro.get_path_row_str_from(self.__active_rois())
        self.__window.lists_window()._set_default_rois_display(rois_str,
                                                               self.__roi_clicked,
                                                               0, 1)
        self.__active_rois_qlist = self.__window.lists_window().rois_list_widget()

    def _set_scenes_display(self):
        scenes_str = sc.get_scene_id_list_from(self.__active_scenes())
        self.__window.lists_window()._set_default_scenes_display(scenes_str,
                                                                 self.__scene_clicked,
                                                                 0, 2)
        self.__gui.main_display_gui().set_image_display(self.__active_scene.thumbnail().band_path())
        self.__active_scenes_qlist = self.__window.lists_window().scenes_list_widget()

    def active_scene(self) -> sc.Scene:
        return self.__active_scene

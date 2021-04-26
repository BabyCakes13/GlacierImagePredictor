#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys

from ui import window as w
from utils import logging

from preprocess.entities import scene as sc
from preprocess.entities import roi as ro
from preprocess.entities import glacier as gl

logger = logging.getLogger(__name__)


class GUI():

    def __init__(self, glaciers):
        self.__app = QtWidgets.QApplication(sys.argv)
        self.__window = w.Window()

        self.__glaciers = glaciers

        self.__active_glacier = self.__glaciers[0]
        self.__active_roi = self.__active_glacier.rois()[0]
        self.__active_scene = self.__active_roi.scenes()[0]

        self.__active_glaciers_qlist = None
        self.__active_rois_qlist = None
        self.__active_scenes_qlist = None

        logger.debug("Created {}.".format(self.__str__()))

    def start(self):
        self.__setup_elements()
        self.__window.show()
        sys.exit(self.__app.exec_())

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
        logger.info("Active scene changed to {}".format(str(self.__active_scene)))

    def __update_rois(self) -> None:
        self.__update_active_roi(self.__active_glacier.rois()[0])
        self.__setup_roi_display()

        self.__update_scenes()

    def __update_scenes(self) -> None:
        self.__update_active_scene(self.__active_roi.scenes()[0])
        self.__setup_scenes_display()

    def __glacier_clicked(self, item):
        item = self.__active_glaciers_qlist.currentItem()
        glacier = gl.find_glacier_by_wgi_id(item.text(), self.__glaciers)

        print(glacier)

        self.__update_active_glacier(glacier)
        self.__update_rois()

    def __roi_clicked(self):
        item = self.__active_rois_qlist.currentItem()
        roi = ro.find_roi_by_path_row(item.text(), self.__active_rois())

        self.__update_active_roi(roi)
        self.__update_scenes()

    def __scene_clicked(self, item: str):
        item = self.__active_scenes_qlist.currentItem()
        scene = sc.find_scene_by_wgi_id(item.text(), self.__active_scenes())

        self.__update_active_scene(scene)
        self.__setup_image_display()

    def __setup_glacier_display(self):
        glaciers_str = [glacier.wgi_id() for glacier in self.__glaciers]
        self.__window._set_default_glaciers_display(glaciers_str,
                                                    self.__glacier_clicked,
                                                    0, 0)
        self.__active_glaciers_qlist = self.__window._glaciers_display()

    def __setup_roi_display(self):
        rois_str = [roi.str_path_row() for roi in self.__active_glacier.rois()]
        self.__window._set_default_rois_display(rois_str,
                                                self.__roi_clicked,
                                                0, 1)
        self.__active_rois_qlist = self.__window._rois_display()

    def __setup_scenes_display(self):
        scenes_str = [scene.scene_id().scene_id() for scene in self.__active_roi.scenes()]
        self.__window._set_default_scenes_display(scenes_str,
                                                  self.__scene_clicked,
                                                  0, 2)
        self.__setup_image_display()
        self.__active_scenes_qlist = self.__window._scenes_display()

    def __setup_image_display(self):
        print("Active scene is {} with red band path {}".format(self.__active_scene, self.__active_scene.red_band().band_path()))
        self.__window._set_image_display(self.__active_scene.red_band().band_path(), 0, 3)

    def __setup_elements(self):
        self.__setup_glacier_display()
        self.__setup_roi_display()
        self.__setup_scenes_display()
        self.__setup_image_display()

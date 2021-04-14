#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets as qt

from ui import window as w
from utils import logging
logger = logging.getLogger(__name__)


class GUI():

    def __init__(self, glaciers):
        self.app = qt.QApplication(sys.argv)
        self.window = w.Window()
        self.__setup_window_size()

        self.__glaciers = glaciers

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_window_size(self):
        screen = self.app.primaryScreen()
        size = screen.size()
        self.window._setup_screen_size(size.width(), size.height())

    def __setup_elements(self):
        default_rois = self.__glaciers[0].rois()
        default_scenes = default_rois[0].scenes()

        self.__setup_glacier_display(self.__glaciers)
        self.__setup_roi_display(default_rois)
        self.__setup_scenes_display(default_scenes)

        scene = default_scenes[0]
        self.__setup_image_display(scene)

    def __setup_glacier_display(self, glaciers):
        glaciers_str = [glacier.wgi_id() for glacier in glaciers]
        self.window._setup_list_display(glaciers_str, 0, 0)

    def __setup_roi_display(self, rois):
        rois_str = [str(roi) for roi in rois]
        self.window._setup_list_display(rois_str, 0, 1)

    def __setup_scenes_display(self, scenes):
        scenes_str = [scene.scene_id().scene_id() for scene in scenes]
        self.window._setup_list_display(scenes_str, 0, 2)

    def __setup_image_display(self, scene):
        self.window._setup_image_display(scene.red_band().band_path(), 0, 3)

    def start(self):
        self.window.window()
        self.__setup_elements()
        self.window.show()
        sys.exit(self.app.exec_())

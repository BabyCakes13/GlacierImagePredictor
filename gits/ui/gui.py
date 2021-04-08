#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets as qt

from ui import window as w
from utils import logging
logger = logging.getLogger(__name__)


class GUI():

    def __init__(self):
        self.app = qt.QApplication(sys.argv)
        self.window = w.Window()

        logger.debug("Created {}.".format(self.__str__()))

    def setup_glacier_display(self, glaciers):
        glaciers_str = [glacier.wgi_id() for glacier in glaciers]
        self.window._setup_list_display(glaciers_str)

    def setup_roi_display(self, rois):
        rois_str = [str(roi) for roi in rois]
        self.window._setup_list_display(rois_str)

    def setup_scenes_display(self, scenes):
        scenes_str = [scene.scene_id().scene_id() for scene in scenes]
        self.window._setup_list_display(scenes_str)

    def start(self):
        self.window.show()
        sys.exit(self.app.exec_())

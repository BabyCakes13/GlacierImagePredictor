#!/usr/bin/env python3
from PyQt5 import QtWidgets
import sys

from ui import window as w
from ui.lists_display import lists_gui
from ui.main_display import main_display_gui
from ui.lists_display.bands import bands_gui

from utils import logging

logger = logging.getLogger(__name__)


class GUI():

    def __init__(self, glaciers):
        self.__app = QtWidgets.QApplication(sys.argv)
        self.__window = w.Window()

        self.__lists_gui = lists_gui.ListsGui(glaciers, self)
        self.__main_display_gui = main_display_gui.MainDisplayGui(self)
        self.__bands_gui = bands_gui.BandsGui(glaciers, self)

        logger.debug("Created {}.".format(self.__str__()))

    def start(self):
        self.__set_default_elements()
        self.__window.show()
        sys.exit(self.__app.exec_())

    def __set_default_elements(self):
        self.__lists_gui._set_glacier_display()
        self.__lists_gui._set_roi_display()
        self.__lists_gui._set_scenes_display()
        self.__bands_gui._set_band_display()

    def window(self) -> QtWidgets.QMainWindow:
        return self.__window

    def lists_gui(self) -> lists_gui.ListsGui:
        return self.__lists_gui

    def main_display_gui(self) -> main_display_gui.MainDisplayGui:
        return self.__main_display_gui

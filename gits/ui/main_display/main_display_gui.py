#!/usr/bin/env python3
from utils import logging
logger = logging.getLogger(__name__)


class MainDisplayGui:
    def __init__(self, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

    def set_image_display(self, image):
        logger.info("Main display showing {}".format(image))
        self.__window.main_display_window()._set_image_viewer(image, 1, 4)

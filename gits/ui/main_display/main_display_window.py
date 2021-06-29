#!/usr/bin/env python3
from entities import image
from ui.main_display import image_viewer


class MainDisplayWindow:
    def __init__(self, layout):
        self.__layout = layout

        self.__image_viewer = image_viewer.ImageViewer()

    def _set_image_viewer(self, image: image.Image):
        self.__image_viewer._update_image(image)
        self.__layout.addWidget(self.__image_viewer.viewer())

    def image_viewer(self):
        return self.__image_viewer

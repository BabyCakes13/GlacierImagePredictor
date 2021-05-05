#!/usr/bin/env python3
from ui.main_display import image_viewer


class MainDisplayWindow:
    def __init__(self, layout):
        self.__layout = layout

        self.__image_viewer = image_viewer.ImageViewer()

    def _set_image_viewer(self, image_filepath: str, grid_row: int, grid_column: int):
        self.__image_viewer._update_image(image_filepath)
        self.__layout.addWidget(self.__image_viewer.viewer(), grid_row, grid_column)

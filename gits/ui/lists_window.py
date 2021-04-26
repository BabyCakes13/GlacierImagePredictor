#!/usr/bin/env python3
from PyQt5 import QtWidgets

from ui import glacier_list_widget
from ui import roi_list_widget
from ui import scene_list_widget


class ListsWindow():
    def __init__(self, layout):
        self.__layout = layout
        self.__glacier_list_widget = None
        self.__roi_list_widget = None
        self.__scene_list_widget = None

    def _set_default_glaciers_display(self, items: list, clicked,
                                      grid_row: int, grid_column: int):
        self.__glacier_list_widget = glacier_list_widget.GlacierListWidget(items, clicked,
                                                                           grid_row, grid_column)
        self.__layout.addWidget(self.__glacier_list_widget.list_widget(), grid_row, grid_column)

    def _set_default_rois_display(self, items: list, clicked,
                                  grid_row: int, grid_column: int):
        self.__roi_list_widget = roi_list_widget.RoiListWidget(items, clicked,
                                                               grid_row, grid_column)
        self.__layout.addWidget(self.__roi_list_widget.list_widget(), grid_row, grid_column)

    def _set_default_scenes_display(self, items: list, clicked,
                                    grid_row: int, grid_column: int):
        self.__scene_list_widget = scene_list_widget.SceneListWidget(items, clicked,
                                                                     grid_row, grid_column)
        self.__layout.addWidget(self.__scene_list_widget.list_widget(), grid_row, grid_column)

    def glaciers_list_widget(self) -> QtWidgets.QListWidget:
        return self.__glacier_list_widget

    def rois_list_widget(self) -> QtWidgets.QListWidget:
        return self.__roi_list_widget

    def scenes_list_widget(self) -> QtWidgets.QListWidget:
        return self.__scene_list_widget

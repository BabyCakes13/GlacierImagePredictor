#!/usr/bin/env python3
from ui.lists_display.glaciers.glacier_list_widget import GlacierListWidget
from ui.lists_display.rois.roi_list_widget import RoiListWidget
from ui.lists_display.scenes.scene_list_widget import SceneListWidget
from ui.lists_display.bands.band_list_widget import BandListWidget
from PyQt5 import QtWidgets


class ListsWindow:
    def __init__(self, layout):
        self.__layout = QtWidgets.QHBoxLayout()
        layout.addLayout(self.__layout)
        self.__glacier_list_widget = None
        self.__roi_list_widget = None
        self.__scene_list_widget = None

    def _set_default_glaciers_display(self, items: list, clicked):
        self.__glacier_list_widget = GlacierListWidget(items, clicked)
        self.__glacier_list_widget.vertical_widget()
        self.__layout.addWidget(self.__glacier_list_widget.widget())

    def _set_default_rois_display(self, items: list, clicked):
        self.__roi_list_widget = RoiListWidget(items, clicked)
        self.__roi_list_widget.vertical_widget()
        self.__layout.addWidget(self.__roi_list_widget.widget())

    def _set_default_scenes_display(self, items: list, clicked):
        self.__scene_list_widget = SceneListWidget(items, clicked)
        self.__scene_list_widget.vertical_widget()
        self.__layout.addWidget(self.__scene_list_widget.widget())

    def _set_default_bands_display(self, items: list, clicked):
        self.__band_list_widget = BandListWidget(items, clicked)
        self.__band_list_widget.vertical_widget()
        self.__layout.addWidget(self.__band_list_widget.widget())

    def glaciers_list_widget(self) -> GlacierListWidget:
        return self.__glacier_list_widget

    def rois_list_widget(self) -> RoiListWidget:
        return self.__roi_list_widget

    def scenes_list_widget(self) -> SceneListWidget:
        return self.__scene_list_widget

    def bands_list_widget(self) -> BandListWidget:
        return self.__band_list_widget

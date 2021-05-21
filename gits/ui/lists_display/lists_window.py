#!/usr/bin/env python3
from ui.lists_display.glaciers.glacier_list_widget import GlacierListWidget
from ui.lists_display.rois.roi_list_widget import RoiListWidget
from ui.lists_display.scenes.scene_list_widget import SceneListWidget
from ui.lists_display.bands.band_list_widget import BandListWidget


class ListsWindow:
    def __init__(self, layout):
        self.__layout = layout
        self.__glacier_list_widget = None
        self.__roi_list_widget = None
        self.__scene_list_widget = None

    def _set_default_glaciers_display(self, items: list, clicked,
                                      grid_row: int, grid_column: int):
        self.__glacier_list_widget = GlacierListWidget(items, clicked,
                                                       grid_row, grid_column)
        self.__glacier_list_widget.vertical_widget()
        self.__layout.addWidget(self.__glacier_list_widget.widget(), grid_row, grid_column)

    def _set_default_rois_display(self, items: list, clicked,
                                  grid_row: int, grid_column: int):
        self.__roi_list_widget = RoiListWidget(items, clicked,
                                               grid_row, grid_column)
        self.__roi_list_widget.vertical_widget()
        self.__layout.addWidget(self.__roi_list_widget.widget(), grid_row, grid_column)

    def _set_default_scenes_display(self, items: list, clicked,
                                    grid_row: int, grid_column: int):
        self.__scene_list_widget = SceneListWidget(items, clicked,
                                                   grid_row, grid_column)
        self.__scene_list_widget.vertical_widget()
        self.__layout.addWidget(self.__scene_list_widget.widget(), grid_row, grid_column)

    def _set_default_bands_display(self, items: list, clicked,
                                   grid_row: int, grid_column: int):
        print(items)
        self.__band_list_widget = BandListWidget(items, clicked,
                                                 grid_row, grid_column)
        self.__band_list_widget.vertical_widget()
        self.__layout.addWidget(self.__band_list_widget.widget(), grid_row, grid_column)

    def glaciers_list_widget(self) -> GlacierListWidget:
        return self.__glacier_list_widget

    def rois_list_widget(self) -> RoiListWidget:
        return self.__roi_list_widget

    def scenes_list_widget(self) -> SceneListWidget:
        return self.__scene_list_widget

    def bands_list_widget(self) -> BandListWidget:
        return self.__band_list_widget

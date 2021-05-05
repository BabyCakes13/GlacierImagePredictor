#!/usr/bin/env python3
from ui.band_list_widget import BandListWidget


class BandWindow:
    def __init__(self, layout):
        self.__layout = layout

        self.__band_list_widget = None

    def _set_bands_display(self, items: list, clicked,
                           grid_row: int, grid_column: int):
        self.__band_list_widget = BandListWidget(items, clicked, grid_row, grid_column)
        self.__band_list_widget.vertical_widget()
        self.__layout.addWidget(self.__band_list_widget.widget(), grid_row, grid_column)

    def band_list_widget(self) -> BandListWidget:
        return self.__band_list_widget

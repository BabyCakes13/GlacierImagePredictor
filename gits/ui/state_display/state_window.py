#!/usr/bin/env python3
from PyQt5 import QtWidgets
from ui.state_display.state_list_widget import StateListWidget

from utils import logging
logger = logging.getLogger(__name__)


class StateWindow:
    def __init__(self, layout):
        self.__layout = layout
        self.__state_list_widget = None

    def _set_default_state_display(self, items: list, clicked,
                                   grid_row: int, grid_column: int):
        self.__state_list_widget = StateListWidget(items, clicked, grid_row, grid_column)
        self.__state_list_widget.horizontal_widget()
        self.__layout.addWidget(self.__state_list_widget.widget(), grid_row, grid_column)

    def state_list_widget(self) -> QtWidgets.QListWidget:
        return self.__state_list_widget

#!/usr/bin/env python3
from PyQt5 import QtWidgets


class EntityListWidget():
    def __init__(self, items: list, clicked, grid_row: int, grid_column: int):
        self._grid_row = grid_row
        self._grid_column = grid_column
        self._clicked = clicked
        self._items = items

        self._set_default_list_widget()

    def _set_default_list_widget(self):
        self._list_widget = QtWidgets.QListWidget()
        self._list_widget.clicked.connect(self._clicked)
        self.__set_list_widget_width(self._items, self._list_widget)
        self._list_widget.addItems(self._items)

    def _update_list_widget_items(self, items: list):
        self._list_widget.clear()
        self._list_widget.addItems(items)
        self._items = items
        self._list_widget.repaint()

    def _add_to_layout(self, layout) -> None:
        layout.addWidget(self._list_widget,
                         self._grid_row,
                         self._grid_column)

    def __set_list_widget_width(self, items, list_widget):
        longest_str_length = max(items, key=len)
        width = list_widget.fontMetrics().boundingRect(longest_str_length).width() + 26
        list_widget.setFixedWidth(width)

    def list_widget(self) -> QtWidgets.QListWidget:
        return self._list_widget

    def grid_row(self) -> int:
        return self._grid_row

    def grid_column(self) -> int:
        return self._grid_column

    def items(self) -> list:
        return self._items

    def current_item(self):
        return self._list_widget.currentItem()

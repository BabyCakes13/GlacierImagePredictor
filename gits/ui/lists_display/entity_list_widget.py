#!/usr/bin/env python3
from PyQt5 import QtWidgets


class EntityListWidget():

    DEFAULT_FONT_SIZE = 30

    def __init__(self, items: list, clicked, grid_row: int, grid_column: int):
        self._grid_row = grid_row
        self._grid_column = grid_column
        self._clicked = clicked
        self._items = items

    def vertical_widget(self):
        self._widget = QtWidgets.QListWidget()
        self._widget.clicked.connect(self._clicked)
        self.__set_fixed_widget_width(self._items, self._widget)
        self._widget.addItems(self._items)

    def horizontal_widget(self):
        self._widget = QtWidgets.QListWidget()
        self._widget.setFlow(QtWidgets.QListView.LeftToRight)
        self.__set_fixed_height(self._widget)
        self._widget.clicked.connect(self._clicked)
        self._widget.addItems(self._items)

    def _update_widget_items(self, items: list):
        self._widget.clear()
        self._widget.addItems(items)
        self._items = items

    def _add_to_layout(self, layout) -> None:
        layout.addWidget(self._widget,
                         self._grid_row,
                         self._grid_column)

    def __set_fixed_widget_width(self, items, widget):
        longest_str_length = max(items, key=len)
        width = widget.fontMetrics().boundingRect(longest_str_length).width() + \
            self.DEFAULT_FONT_SIZE
        widget.setFixedWidth(width)

    def __set_fixed_height(self, widget):
        widget.setFixedHeight(self.DEFAULT_FONT_SIZE)

    def widget(self) -> QtWidgets.QListWidget:
        return self._widget

    def grid_row(self) -> int:
        return self._grid_row

    def grid_column(self) -> int:
        return self._grid_column

    def items(self) -> list:
        return self._items

    def current_item(self):
        return self._widget.currentItem()

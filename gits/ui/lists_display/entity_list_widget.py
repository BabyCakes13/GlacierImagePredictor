#!/usr/bin/env python3
from PyQt5 import QtWidgets


class EntityListWidget():

    DEFAULT_FONT_SIZE = 30

    def __init__(self, items: list, clicked):
        self._clicked = clicked
        self._items = items

        self._widget = self.__create_basic_widget()

    def __create_basic_widget(self):
        widget = QtWidgets.QListWidget()
        widget.clicked.connect(self._clicked)
        widget.addItems(self._items)

        return widget

    def vertical_widget(self):
        self.__fixed_vertical_width()

    def horizontal_widget(self):
        self._widget.setFlow(QtWidgets.QListView.LeftToRight)
        self.__fixed_horizontal_width()
        self._widget.setFixedHeight(self.DEFAULT_FONT_SIZE)

    def _update_widget_items(self, items: list):
        self._widget.clear()
        self._widget.addItems(items)
        self._items = items

    def _add_to_layout(self, layout) -> None:
        layout.addWidget(self._widget,
                         self._grid_row,
                         self._grid_column)

    def __fixed_vertical_width(self):
        longest_item = max(self._items, key=len)
        width = self._widget.fontMetrics().boundingRect(longest_item).width() + \
            self.DEFAULT_FONT_SIZE
        self._widget.setFixedWidth(width)

    def __fixed_horizontal_width(self):
        concatenated_items = ''.join(self._items)
        width = self._widget.fontMetrics().boundingRect(concatenated_items).width() + \
            self.DEFAULT_FONT_SIZE
        self._widget.setFixedWidth(width)

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

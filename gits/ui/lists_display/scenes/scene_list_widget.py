#!/usr/bin/env python3

from ui.lists_display import entity_list_widget


class SceneListWidget(entity_list_widget.EntityListWidget):
    def __init__(self, items: list, clicked, grid_row: int, grid_column: int):
        super().__init__(items, clicked, grid_row, grid_column)

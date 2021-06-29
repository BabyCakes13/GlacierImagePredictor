#!/usr/bin/env python3

from ui.lists_display import entity_list_widget


class RoiListWidget(entity_list_widget.EntityListWidget):
    def __init__(self, items: list, clicked):
        super().__init__(items, clicked)

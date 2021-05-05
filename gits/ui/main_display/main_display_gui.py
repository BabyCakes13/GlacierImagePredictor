#!/usr/bin/env python3

class MainDisplayGui:
    def __init__(self, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

    def set_image_display(self, image):
        self.__window.main_display_window()._set_image_viewer(image, 0, 4)

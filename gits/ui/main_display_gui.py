#!/usr/bin/env python3

class MainDisplayGui:
    def __init__(self, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

    def set_image_display(self):
        active_scene = self.__gui.lists_gui().active_scene()
        self.__window.main_display_window()._set_image_viewer(active_scene.red_band()
                                                              .band_path(), 0, 3)

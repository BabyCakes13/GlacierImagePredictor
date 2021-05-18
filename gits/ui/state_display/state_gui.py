#!/usr/bin/env python3
from utils import logging
logger = logging.getLogger(__name__)


class StateGui:
    AVAILABLE_STATES = ["Aligned Scenes", "Unaligned Scenes"]

    def __init__(self, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

    def _set_state_display(self):
        self.__window.state_window()._set_default_state_display(self.AVAILABLE_STATES,
                                                                self.__state_clicked,
                                                                0, 0)

    def __state_clicked(self):
        logger.debug("Clicked new state.")

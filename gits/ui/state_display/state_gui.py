#!/usr/bin/env python3
from utils import logging
logger = logging.getLogger(__name__)


class StateGui:
    AVAILABLE_STATES = ["Aligned", "Unaligned"]
    ACTIVE_STATE = "Unaligned"

    def __init__(self, gui):
        self.__gui = gui
        self.__window = self.__gui.window()

        self.__active_state = self.ACTIVE_STATE

    def __update_active_state(self, state) -> None:
        logger.info("State changed from {} to {}".format(self.__active_state, state))
        self.__active_state = state

    def _set_state_display(self):
        self.__window.state_window()._set_default_state_display(self.AVAILABLE_STATES,
                                                                self.__state_clicked,
                                                                0, 0)
        self.__state_list_widget = self.__window.state_window().state_list_widget()

    def __state_clicked(self):
        state = self.__state_list_widget.current_item().text()
        self.__update_active_state(state)

from PyQt5 import QtWidgets

from ui import lists_window
from ui import main_display_window
from ui import bands_window

from utils import logging
logger = logging.getLogger(__name__)


class Window():
    def __init__(self):
        self.__window = QtWidgets.QMainWindow()
        self.__setup_elements()

        self.__lists_window = lists_window.ListsWindow(self.__layout)
        self.__main_display_windw = main_display_window.MainDisplayWindow(self.__layout)
        self.__bands_window = bands_window.BandWindow(self.__layout)

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_elements(self):
        self.__set_layout()
        self.__set_central_widget()
        self.__set_window("GUI")
        self.__set_menu()

    def __set_window(self, title: str) -> None:
        self.__window.setWindowTitle(title)

    def __set_layout(self) -> None:
        self.__layout = QtWidgets.QGridLayout()

    def __set_central_widget(self) -> None:
        widget = QtWidgets.QWidget()
        widget.setLayout(self.__layout)
        self.__window.setCentralWidget(widget)

    def _set_timeline_display(self):
        # TODO Not sure whether to display dates or thumbnails here. Would make more sense to
        # display the dates somehow, since the image is super small and we won't notive anyway
        # details from the thumbnail. But thumbnail looks better. Eh.
        pass

    def __set_menu(self) -> None:
        self.menu = self.__window.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.__window.close)

    def __set_toolbar(self):
        tools = QtWidgets.QToolBar()
        self.__window.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def lists_window(self) -> lists_window.ListsWindow:
        return self.__lists_window

    def main_display_window(self) -> main_display_window.MainDisplayWindow:
        return self.__main_display_windw

    def bands_window(self) -> bands_window.BandWindow:
        return self.__bands_window

    def show(self):
        self.__window.show()

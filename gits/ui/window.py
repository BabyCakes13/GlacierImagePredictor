from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qg

from utils import logging
logger = logging.getLogger(__name__)


class Window(qtw.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.__setup_layout()
        self.__setup_elements()

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_elements(self) -> None:
        self.__set_central_widget()
        self.__setup_window("GUI")
        self.__setup_menu()
        # self.__setup_toolbar()

    def __setup_window(self, title: str) -> None:
        self.setWindowTitle(title)
        self.showMaximized()

    def __setup_layout(self) -> None:
        self.__layout = qtw.QGridLayout()

        # glacier display
        self.__layout.setColumnStretch(0, 1)
        # region of interest display
        self.__layout.setColumnStretch(1, 1)
        # scenes display
        self.__layout.setColumnStretch(2, 1)
        # image display
        self.__layout.setColumnStretch(3, 3)

    def __set_central_widget(self) -> None:
        widget = qtw.QWidget()
        widget.setLayout(self.__layout)
        self.setCentralWidget(widget)

    def _setup_list_display(self, items: list, grid_row: int, grid_column: int) -> None:
        list_widget = qtw.QListWidget()
        list_widget.addItems(items)

        # TODO find a better way to calculate the width such that each charagter is displayed
        # for now, the + 26 makes sure that the whole word fits into the list view.
        longest_str_length = max(items, key=len)
        width = list_widget.fontMetrics().boundingRect(longest_str_length).width() + 26
        list_widget.setFixedWidth(width)

        self.__layout.addWidget(list_widget, grid_row, grid_column)

    def get_items(self, list_widget):
        items = []
        for index in range(list_widget.count()):
            items.append(list_widget.item(index))

        return items

    def _setup_image_display(self, image):
        pass

    def _setup_timeline_display(self):
        pass

    def __setup_menu(self) -> None:
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def __setup_toolbar(self):
        tools = qtw.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore

from utils import logging
logger = logging.getLogger(__name__)


class Window(qtw.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.__setup_layout()
        self.__set_central_widget()
        self.__setup_window("GUI")
        self.__setup_menu()

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_window(self, title: str) -> None:
        self.setWindowTitle(title)

    def _setup_screen_size(self, width, height):
        self.setFixedSize(width, height)

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
        self.__layout.setRowStretch(3, 2)

    def __set_central_widget(self) -> None:
        widget = qtw.QWidget()
        widget.setLayout(self.__layout)
        self.setCentralWidget(widget)

    def _setup_list_display(self, items: list, grid_row: int, grid_column: int) -> None:
        list_widget = qtw.QListWidget()
        list_widget.addItems(items)

        # TODO find a better way to calculate the width such that each character is displayed
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

    def _setup_image_display(self, image, grid_row, grid_column):
        """
        Function which represents the main image screen of the GUI.

        This will hold the glacier high scale image, possible graphs and interaction.
        """
        image = qg.QPixmap(image)
        label = qtw.QLabel()
        image = image.scaled(self.__image_width(),
                             self.__image_height(),
                             QtCore.Qt.KeepAspectRatio)
        label.setPixmap(image)

        self.__layout.addWidget(label, grid_row, grid_column)

    def image_width(self) -> int:
        return (self.width() / 8) * 10

    def __image_height(self) -> int:
        return (self.height() / 8) * 7

    def _setup_timeline_display(self):
        # TODO Not sure whether to display dates or thumbnails here. Would make more sense to
        # display the dates somehow, since the image is super small and we won't notive anyway
        # details from the thumbnail. But thumbnail looks better. Eh.
        pass

    def __setup_menu(self) -> None:
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def __setup_toolbar(self):
        tools = qtw.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

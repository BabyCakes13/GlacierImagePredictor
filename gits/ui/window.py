from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

from ui.PyQtImageViewer.QtImageViewer import QtImageViewer

from utils import logging
logger = logging.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
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
        self.__width = width
        self.__height = height

    def __setup_layout(self) -> None:
        self.__layout = QtWidgets.QGridLayout()

    def __set_central_widget(self) -> None:
        widget = QtWidgets.QWidget()
        widget.setLayout(self.__layout)
        self.setCentralWidget(widget)

    def _setup_list_display(self, items: list, clicked, grid_row: int, grid_column: int) -> None:
        list_widget = QtWidgets.QListWidget()
        list_widget.addItems(items)

        # TODO find a better way to calculate the width such that each character is displayed
        # for now, the + 26 makes sure that the whole word fits into the list view.
        longest_str_length = max(items, key=len)
        width = list_widget.fontMetrics().boundingRect(longest_str_length).width() + 26
        list_widget.setFixedWidth(width)
        list_widget.clicked.connect(clicked)

        self.__layout.addWidget(list_widget, grid_row, grid_column)

        return list_widget

    def get_items(self, list_widget):
        items = []
        for index in range(list_widget.count()):
            items.append(list_widget.item(index))

        return items

    def _setup_image_display(self, image_filepath, grid_row, grid_column):
        """
        Function which represents the main image screen of the GUI.

        This will hold the glacier high scale image, possible graphs and interaction.
        """
        viewer = QtImageViewer()
        viewer.aspectRatioMode = QtCore.Qt.KeepAspectRatio
        viewer.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        viewer.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        viewer.canZoom = True
        viewer.canPan = True

        image = QtGui.QImage(image_filepath)
        viewer.setImage(image)
        viewer.show()

        self.__layout.addWidget(viewer, grid_row, grid_column)

    def _setup_timeline_display(self):
        # TODO Not sure whether to display dates or thumbnails here. Would make more sense to
        # display the dates somehow, since the image is super small and we won't notive anyway
        # details from the thumbnail. But thumbnail looks better. Eh.
        pass

    def __setup_menu(self) -> None:
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def __setup_toolbar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

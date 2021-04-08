from PyQt5 import QtWidgets as qt

from utils import logging
logger = logging.getLogger(__name__)


class Window(qt.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.__layout = qt.QHBoxLayout()
        self.__set_central_widget()
        self.__setup_window()
        self.__setup_menu()
        self.__setup_toolbar()

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_window(self):
        self.setWindowTitle("Cool title to be.")
        self.showMaximized()

    def __set_central_widget(self):
        widget = qt.QWidget()
        widget.setLayout(self.__layout)
        self.setCentralWidget(widget)

    def _setup_list_display(self, items):
        list_widget = qt.QListWidget()
        list_widget.addItems(items)

        self.__layout.addWidget(list_widget)

    def _setup_image_display(self):
        pass

    def _setup_timeline_display(self):
        pass

    def __setup_menu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def __setup_toolbar(self):
        tools = qt.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def window(self):
        return self.__window

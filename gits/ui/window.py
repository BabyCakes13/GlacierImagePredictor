from PyQt5 import QtWidgets

from ui.lists_display import lists_window
from ui.main_display import main_display_window
from ui.state_display import state_window
from ui.ndsi_plot import ndsi_plot

from utils import logging
logger = logging.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__setup_elements()

        self.__state_window = state_window.StateWindow(self.__menu_layout)
        self.__lists_window = lists_window.ListsWindow(self.__menu_layout)
        self.__ndsi_plot = ndsi_plot.NdsiPlot(self.__menu_layout)
        self.__main_display_windw = main_display_window.MainDisplayWindow(self.__main_layout)

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_elements(self):
        self.__set_layout()
        self.__set_central_widget()
        self.__set_window("GUI")
        self.__set_menu()

    def __set_window(self, title: str) -> None:
        self.setWindowTitle(title)

    def __set_layout(self) -> None:
        self.__main_layout = QtWidgets.QHBoxLayout()
        self.__menu_layout = QtWidgets.QVBoxLayout()

        self.__main_layout.addLayout(self.__menu_layout)

    def __set_central_widget(self) -> None:
        widget = QtWidgets.QWidget()
        widget.setLayout(self.__main_layout)
        self.setCentralWidget(widget)

    def _set_timeline_display(self):
        # TODO Not sure whether to display dates or thumbnails here. Would make more sense to
        # display the dates somehow, since the image is super small and we won't notive anyway
        # details from the thumbnail. But thumbnail looks better. Eh.
        pass

    def __save(self):

        suggestedFileName = self.__main_display_windw.image_viewer().name() + ".tiff"
        suggestedFilePath = "/tmp/"

        fileName, typefilter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save F:xile",
            suggestedFilePath + suggestedFileName,
            "Images (*.tiff *.png)")
        self.__main_display_windw.image_viewer().save(fileName)

    def createAction(self, name, shortcut, function):
        act = QtWidgets.QAction(name, self)
        act.setShortcut(shortcut)
        act.triggered.connect(function)
        return act

    def __set_menu(self) -> None:
        self.menu = self.menuBar().addMenu("&Menu")

        self.menu.addAction(self.createAction('&Save', "Ctrl+S", self.__save))
        self.menu.addAction(self.createAction('&Exit', "Ctrl+Q", self.close))

    def __set_toolbar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def lists_window(self) -> lists_window.ListsWindow:
        return self.__lists_window

    def main_display_window(self) -> main_display_window.MainDisplayWindow:
        return self.__main_display_windw

    def state_window(self) -> state_window.StateWindow:
        return self.__state_window

    def ndsi_plot(self):
        return self.__ndsi_plot

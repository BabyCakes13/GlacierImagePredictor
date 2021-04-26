from PyQt5 import QtWidgets

from ui import image_viewer
from ui import glacier_list_widget
from ui import roi_list_widget
from ui import scene_list_widget

from utils import logging
logger = logging.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.__setup_elements()

        self.__glacier_list_widget = None
        self.__roi_list_widget = None
        self.__scene_list_widget = None
        self.__image_display = None

        logger.debug("Created {}.".format(self.__str__()))

    def __setup_elements(self):
        self.__set_layout()
        self.__set_central_widget()
        self.__set_window("GUI")
        self.__set_menu()

    def __set_window(self, title: str) -> None:
        self.setWindowTitle(title)

    def __set_layout(self) -> None:
        self.__layout = QtWidgets.QGridLayout()

    def __set_central_widget(self) -> None:
        widget = QtWidgets.QWidget()
        widget.setLayout(self.__layout)
        self.setCentralWidget(widget)

    def _set_default_glaciers_display(self, items: list, clicked, grid_row: int, grid_column: int):
        self.__glacier_list_widget = glacier_list_widget.GlacierListWidget(items, clicked,
                                                                           grid_row, grid_column)
        self.__layout.addWidget(self.__glacier_list_widget.list_widget(),
                                self.__glacier_list_widget.grid_row(),
                                self.__glacier_list_widget.grid_column())

    def _set_default_rois_display(self, items: list, clicked, grid_row: int, grid_column: int):
        self.__roi_list_widget = roi_list_widget.RoiListWidget(items, clicked,
                                                               grid_row, grid_column)
        self.__layout.addWidget(self.__roi_list_widget.list_widget(),
                                self.__roi_list_widget.grid_row(),
                                self.__roi_list_widget.grid_column())

    def _set_default_scenes_display(self, items: list, clicked, grid_row: int, grid_column: int):
        self.__scene_list_widget = scene_list_widget.SceneListWidget(items, clicked,
                                                                     grid_row, grid_column)
        self.__layout.addWidget(self.__scene_list_widget.list_widget(),
                                self.__scene_list_widget.grid_row(),
                                self.__scene_list_widget.grid_column())

    def _set_image_display(self, image_filepath, grid_row, grid_column):
        self.__image_viewer = image_viewer.ImageViewer(image_filepath)
        self.__layout.addWidget(self.__image_viewer.viewer(), grid_row, grid_column)

    def _set_timeline_display(self):
        # TODO Not sure whether to display dates or thumbnails here. Would make more sense to
        # display the dates somehow, since the image is super small and we won't notive anyway
        # details from the thumbnail. But thumbnail looks better. Eh.
        pass

    def __set_menu(self) -> None:
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)

    def __set_toolbar(self):
        tools = QtWidgets.QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _glaciers_display(self) -> QtWidgets.QListWidget:
        return self.__glacier_list_widget

    def _rois_display(self) -> QtWidgets.QListWidget:
        return self.__roi_list_widget

    def _scenes_display(self) -> QtWidgets.QListWidget:
        return self.__scene_list_widget

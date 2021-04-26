from PyQt5 import QtWidgets
from ui.image_viewer import ImageViewer

from utils import logging
logger = logging.getLogger(__name__)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.__setup_elements()

        self.__glaciers_display = None
        self.__rois_display = None
        self.__scenes_display = None
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

    def __set_default_list_display(self, items: list,
                                   clicked,
                                   grid_row: int, grid_column: int) -> QtWidgets.QListWidget:
        list_widget = QtWidgets.QListWidget()
        list_widget.addItems(items)
        list_widget.clicked.connect(clicked)

        return list_widget

    def _set_default_glaciers_display(self, glaciers: list, clicked,
                                      grid_row: int, grid_column: int) -> None:
        self.__glaciers_display = self.__set_default_list_display(glaciers, clicked,
                                                                  grid_row, grid_column)
        self.__set_list_widget_width(glaciers, self.__glaciers_display)
        self.__layout.addWidget(self.__glaciers_display, grid_row, grid_column)

    def _set_default_rois_display(self, rois: list, clicked,
                                  grid_row: int, grid_column: int) -> None:
        self.__rois_display = self.__set_default_list_display(rois, clicked,
                                                              grid_row, grid_column)
        self.__set_list_widget_width(rois, self.__rois_display)
        self.__layout.addWidget(self.__rois_display, grid_row, grid_column)

    def _set_default_scenes_display(self, scenes: list, clicked,
                                    grid_row: int, grid_column: int) -> None:
        self.__scenes_display = self.__set_default_list_display(scenes, clicked,
                                                                grid_row, grid_column)
        self.__set_list_widget_width(scenes, self.__scenes_display)
        self.__layout.addWidget(self.__scenes_display, grid_row, grid_column)

    def _update_rois_display(self, rois_str_format: list) -> None:
        self.__rois_display.clear()
        self.__rois_display.addItems(rois_str_format)
        self.__rois_display.repaint()

    def _update_scenes_display(self, scenes_str_format: list) -> None:
        self.__scenes_display.clear()
        self.__scenes_display.addItems(scenes_str_format)
        self.__scenes_display.repaint()

    def __set_list_widget_width(self, items, list_widget):
        # TODO find a better way to calculate the width such that each character is displayed
        # for now, the + 26 makes sure that the whole word fits into the list view.
        longest_str_length = max(items, key=len)
        width = list_widget.fontMetrics().boundingRect(longest_str_length).width() + 26
        list_widget.setFixedWidth(width)

    def _set_image_display(self, image_filepath, grid_row, grid_column):
        """
        Function which represents the main image screen of the GUI.

        This will hold the glacier high scale image, possible graphs and interaction.
        """
        self.__image_viewer = ImageViewer()
        self.__image_viewer._update_image(image_filepath)
        self.__layout.addWidget(self.__image_viewer.viewer(), grid_row, grid_column)

    def _update_image(self, image_filepath) -> None:
        self.__image_viewer._update_image(image_filepath)

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

    def get_list_widget_items(self, list_widget: QtWidgets.QListWidget) -> list:
        items = []
        for index in range(list_widget.count()):
            items.append(list_widget.item(index))

        return items

    def _glaciers_display(self) -> QtWidgets.QListWidget:
        return self.__glaciers_display

    def _rois_display(self) -> QtWidgets.QListWidget:
        return self.__rois_display

    def _scenes_display(self) -> QtWidgets.QListWidget:
        return self.__scenes_display

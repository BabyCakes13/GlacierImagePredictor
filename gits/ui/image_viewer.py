#!/usr/bin/env python3
from PyQt5 import QtGui
from PyQt5 import QtCore

from ui.PyQtImageViewer.QtImageViewer import QtImageViewer

from utils import logging
logger = logging.getLogger(__name__)


class ImageViewer:
    def __init__(self):
        self.__viewer = self.__set_image_viewer()

    def __set_image_viewer(self) -> QtImageViewer:
        viewer = QtImageViewer()
        viewer.aspectRatioMode = QtCore.Qt.KeepAspectRatio
        viewer.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        viewer.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        viewer.canZoom = True
        viewer.canPan = True

        return viewer

    def _update_image(self, image_filepath):
        image = QtGui.QImage(image_filepath)
        self.__viewer.setImage(image)
        self.__viewer.show()

    def viewer(self) -> QtImageViewer:
        return self.__viewer

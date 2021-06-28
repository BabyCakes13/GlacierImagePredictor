#!/usr/bin/env python3
from PyQt5 import QtGui
from PyQt5 import QtCore

from ui.PyQtImageViewer.QtImageViewer import QtImageViewer

from utils import logging
logger = logging.getLogger(__name__)


class ImageViewer:
    def __init__(self):
        self.__viewer = self.__set_image_viewer()
        self.__image_name = None
        self.__qimage = None

    def __set_image_viewer(self) -> QtImageViewer:
        viewer = QtImageViewer()
        viewer.aspectRatioMode = QtCore.Qt.KeepAspectRatio
        viewer.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        viewer.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        viewer.canZoom = True
        viewer.canPan = True

        return viewer

    def _update_image(self, image):
        self.__image_name = image.scene_name() + "_" + image.name()
        ndarray = image.visual_data()
        ndarray_dimension = len(ndarray.shape)
        width = ndarray.shape[1]
        height = ndarray.shape[0]

        if(ndarray_dimension == 3):
            bytes_per_line = width * 3
            image_format = QtGui.QImage.Format_RGB888
        elif (ndarray_dimension == 2):
            bytes_per_line = width * 2
            image_format = QtGui.QImage.Format_Grayscale16
        else:
            print("Cannot handle image on {} channels.".format(ndarray_dimension))
            # TODO handle this error properly
            return

        self.__qimage = QtGui.QImage(ndarray, width, height, bytes_per_line, image_format)
        self.__viewer.setImage(self.__qimage)
        self.__viewer.show()

    def viewer(self) -> QtImageViewer:
        return self.__viewer

    def name(self):
        return self.__image_name

    def save(self, filename):
        return self.__qimage.save(filename)

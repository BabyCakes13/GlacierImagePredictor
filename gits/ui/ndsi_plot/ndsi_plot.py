#!/usr/bin/env python3

from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
import numpy


class NdsiPlot():
    def __init__(self, layout):
        self.__frame = QtWidgets.QFrame()
        layout.addWidget(self.__frame)
        self.__layout = QtWidgets.QVBoxLayout()
        self.__frame.setLayout(self.__layout)
        self.__roi = None
        self.__glacier_nane = ""

        self.__initialize_buttons()
        self.__initializePlot()

        self.visible(False)

    def __initialize_buttons(self):
        self.__button_layout = QtWidgets.QHBoxLayout()
        nb = QtWidgets.QPushButton("Show NDSI", self.__frame)
        nb.clicked.connect(self.__calculateNDSI)
        gnb = QtWidgets.QPushButton("Show Generated NDSI", self.__frame)
        gnb.clicked.connect(self.__calculateGeneratedNDSI)

        self.__button_layout.addWidget(nb)
        self.__button_layout.addWidget(gnb)

        self.__layout.addLayout(self.__button_layout)

    def __initializePlot(self):
        self.__static_canvas = FigureCanvas(Figure(figsize=(7, 4)))
        self.__layout.addWidget(self.__static_canvas)
        self.__axes = self.__static_canvas.figure.subplots()

    def setGlacier(self, glacier_name):
        self.__glacier_nane = glacier_name

    def setROI(self, roi):
        self.__roi = roi
        if self.__axes is not None:
            self.__axes.remove()
            self.__axes = self.__static_canvas.figure.subplots()
            self.__axes.set_title(self.__glacier_nane + " @ " + str(self.__roi.path()) \
                                  + ":" + str(self.__roi.row()) \
                                  + " Month: " + str(self.__roi.monthrange()[0]))
        self.__static_canvas.draw()

    def visible(self, visible):
        self.__frame.setVisible(visible)

    def __ndsi_series(self):
        s = {}
        for scene in self.__roi.aligned_scenes():
            key = scene.scene_id().date()
            s[key] = scene.ndsi().snow_percentage()

        return s

    def __calculateNDSI(self):
        series = self.__ndsi_series()

        ndsi_values = series.values()
        scens_dates = series.keys()

        print(ndsi_values)
        print(scens_dates)

        self.__axes.plot(scens_dates, ndsi_values, 'go-', label='NDSI')
        offset = (max(ndsi_values) - min(ndsi_values)) / 40
        for scene, ndsi in series.items():
            self.__axes.text(scene, ndsi+offset, "%f" % ndsi, ha="center")
        self.__axes.legend()
        self.__static_canvas.draw()

    def __predicted_ndsi_series(self):
        s = {}
        for scene in self.__roi.aligned_scenes():
            if not hasattr(scene.motion_predicted_ndsi(), 'snow_percentage'):
                lastscene = scene
                continue
            datepredicted = scene.scene_id().date() - lastscene.scene_id().date()
            key = scene.scene_id().date() + datepredicted
            s[key] = scene.motion_predicted_ndsi().snow_percentage()
            lastscene = scene

        return s

    def __calculateGeneratedNDSI(self):
        series = self.__predicted_ndsi_series()

        ndsi_values = series.values()
        scens_dates = series.keys()

        print(ndsi_values)
        print(scens_dates)

        self.__axes.plot(scens_dates, ndsi_values, 'ro-', label='PredictedNDSI')
        offset = (max(ndsi_values) - min(ndsi_values)) / 40
        for scene, ndsi in series.items():
            self.__axes.text(scene, ndsi+offset, "%f" % ndsi, ha="center")
        self.__axes.legend()
        self.__static_canvas.draw()

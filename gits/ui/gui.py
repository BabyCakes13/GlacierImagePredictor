#!/usr/bin/env python3
import sys
from PyQt5 import QtWidgets as qt

from ui import window as w
from utils import logging
logger = logging.getLogger(__name__)


class GUI():

    def __init__(self):
        self.app = qt.QApplication(sys.argv)
        self.window = w.Window()

        logger.debug("Created {}.".format(self.__str__()))

    def start(self):
        self.window.show()
        sys.exit(self.app.exec_())

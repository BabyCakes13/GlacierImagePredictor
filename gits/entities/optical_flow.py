#!/usr/bin/env python3
import cv2
import numpy

from utils import logging
logger = logging.getLogger(__name__)


class OpticalFlow:
    def __init__(self, first_image, second_image):
        self.__first_image = first_image
        self.__second_image = second_image

    def movement(self):
        flow = cv2.calcOpticalFlowFarneback(self.__first_image,
                                            self.__second_image,
                                            None, 0.5, 3, 15, 3, 5, 1.2, 0)
        logger.notice("Maximum element from flow: {}.".format(numpy.amax(flow)))
        logger.notice("0 from flow: {}".format(flow[5000][4000][0]))
        logger.notice("1 from flow: {}".format(flow[5000][4000][1]))
        return flow

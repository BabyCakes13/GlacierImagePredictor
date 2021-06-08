#!/usr/bin/env python3
import cv2
import numpy

from entities.image import Image
from utils import logging
logger = logging.getLogger(__name__)


class OpticalFlow(Image):

    NAME = "Optical Flow"

    def __init__(self, first_image: Image, second_image: Image):
        self.__first_image = first_image
        self.__second_image = second_image

        self.__optical_flow_image = None

    def ndarray(self) -> numpy.ndarray:
        return self.hsv_optical_flow()

    def optical_flow(self):
        flow = cv2.calcOpticalFlowFarneback(self.__first_image.ndarray(),
                                            self.__second_image.ndarray(),
                                            None, 0.5, 3, 15, 3, 5, 1.2, 0)
        logger.notice("Maximum element from flow: {}.".format(numpy.amax(flow)))
        logger.notice("0 from flow: {}".format(flow[5000][4000][0]))
        logger.notice("1 from flow: {}".format(flow[5000][4000][1]))
        return flow

    def hsv_optical_flow(self):
        image1_c = cv2.cvtColor(self.__first_image.ndarray(), cv2.COLOR_GRAY2BGR)
        hsv = numpy.zeros_like(image1_c).astype(numpy.uint8)

        optical_flow = self.optical_flow()
        magnitude, angle = cv2.cartToPolar(optical_flow[..., 0], optical_flow[..., 1])

        # color map
        hsv[..., 0] = angle * 180 / numpy.pi / 2
        hsv[..., 1] = 255
        hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        hsv[..., 2] = self.scale(hsv[..., 2], 3)

        # brighten up
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return bgr

    @staticmethod
    def scale(image, value) -> numpy.ndarray:
        """
        Brighten and contrast up the optical flow image for visual interpretation;
        Remove overflow brightness form the image resulting after optical flow computation.
        Since the values are maximum 255, an overflow would turn those pixels black, aka the lowest level of brightness.
        :param image: The overflowed image.
        :param value: The value of brighten up.
        :return: The improved image.
        """
        image32 = image.astype(numpy.int32)
        image32 = image32 * value
        numpy.clip(image32, 0, 255, out=image32)

        return image32.astype(numpy.uint8)

    def name(self) -> str:
        return self.NAME

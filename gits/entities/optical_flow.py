#!/usr/bin/env python3
import cv2
import numpy

from utils.utils import debug_trace

from entities.image import Image
from utils import logging
logger = logging.getLogger(__name__)


class OpticalFlow(Image):

    NAME = "Optical Flow"

    def __init__(self, first_image: Image, second_image: Image):
        self.__first_image = first_image
        self.__second_image = second_image

        logger.notice("First image: {}\nSecond image: {}".format(self.__first_image,
                                                                 self.__second_image))

        self.__optical_flow_image = None

    def ndarray(self) -> numpy.ndarray:
        return self.hsv_optical_flow()

    def optical_flow(self, first_image_ndarray, second_image_ndarray):
        flow = cv2.calcOpticalFlowFarneback(first_image_ndarray,
                                            second_image_ndarray,
                                            None, 0.5, 3, 15, 3, 5, 1.2, 0)
        logger.notice("Maximum element from flow: {}.".format(numpy.amax(flow)))
        logger.notice("0 from flow: {}".format(flow[5000][4000][0]))
        logger.notice("1 from flow: {}".format(flow[5000][4000][1]))
        return flow

    def hsv_optical_flow(self):
        first_mask = self.create_mask(self.__first_image.ndarray())
        second_mask = self.create_mask(self.__second_image.ndarray())

        optical_flow = self.optical_flow(self.__first_image.ndarray(),
                                         self.__second_image.ndarray())
        magnitude, angle = cv2.cartToPolar(optical_flow[..., 0], optical_flow[..., 1])

        magnitude = numpy.ma.masked_array(magnitude, mask=first_mask).filled(0)
        magnitude = numpy.ma.masked_array(magnitude, mask=second_mask).filled(0)

        colored_clone = cv2.cvtColor(self.__first_image.ndarray(), cv2.COLOR_GRAY2BGR)
        hsv = numpy.zeros_like(colored_clone).astype(numpy.uint8)

        hsv[..., 0] = angle * 180 / numpy.pi / 2
        hsv[..., 1] = 255
        hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        # hsv[..., 2] = self.scale(hsv[..., 2], 10)
        # hsv[..., 2] = 255

        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        return bgr

    @staticmethod
    def scale(image, value) -> numpy.ndarray:
        image32 = image.astype(numpy.int32)
        image32 = image32 * value
        numpy.clip(image32, 0, 255, out=image32)

        return image32.astype(numpy.uint8)

    def name(self) -> str:
        return self.NAME

    def create_mask(self, image):
        ret, threshold = cv2.threshold(image, 1, 0xFFFF, cv2.THRESH_BINARY_INV)

        return threshold

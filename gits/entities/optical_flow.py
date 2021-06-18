#!/usr/bin/env python3
import time
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
        self.__first_mask, self.__second_mask = self.mask_images()
        self.__optical_flow_image = None
        self.__optical_flow = None

    def ndarray(self) -> numpy.ndarray:
        if self.__optical_flow_image is None:
            self.__optical_flow_image = self.hsv_optical_flow()
        return self.__optical_flow_image

    def mask_images(self) -> None:
        first_mask = self.create_mask(self.__first_image.ndarray())
        second_mask = self.create_mask(self.__second_image.ndarray())
        return first_mask, second_mask

    def optical_flow(self) -> numpy.ndarray:
        if self.__optical_flow is None:
            self.__compute_optical_flow()
        return self.__optical_flow

    def __compute_optical_flow(self):
        tik = time.process_time()
        masked_first_image = numpy.ma.masked_array(self.__first_image.ndarray(),
                                                   mask=self.__second_mask).filled(0)
        masked_second_image = numpy.ma.masked_array(self.__second_image.ndarray(),
                                                    mask=self.__first_mask).filled(0)

        self.__optical_flow = cv2.calcOpticalFlowFarneback(masked_first_image,
                                                           masked_second_image,
                                                           None, 0.5, 6, 15, 3, 5, 1.2, 0)
        tok = time.process_time()
        logger.success("Finished optical flow in {} seconds.".format(tok - tik))

    def hsv_optical_flow(self):
        optical_flow = self.optical_flow()
        magnitude, angle = cv2.cartToPolar(optical_flow[..., 0], optical_flow[..., 1])

        magnitude = numpy.ma.masked_array(magnitude, mask=self.__first_mask).filled(0)
        magnitude = numpy.ma.masked_array(magnitude, mask=self.__second_mask).filled(0)

        colored_clone = cv2.cvtColor(self.__first_image.ndarray(), cv2.COLOR_GRAY2BGR)
        hsv = numpy.zeros_like(colored_clone).astype(numpy.uint8)

        hsv[..., 0] = angle * 180 / numpy.pi / 2
        hsv[..., 1] = 255
        hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        hsv[..., 2] = self.scale(hsv[..., 2], 3)
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

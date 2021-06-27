#!/usr/bin/env python3
import time
import cv2
import numpy

from entities.aligned.aligned_image import AlignedImage
from entities.image import Image
from utils import logging
logger = logging.getLogger(__name__)


class MotionVectors(Image):

    NAME = "Motion Vectros"

    def __init__(self, first_image: AlignedImage, second_image: AlignedImage):
        self.__first_image = first_image
        self.__second_image = second_image
        self.__optical_flow = None
        self.__first_mask = None
        self.__second_mask = None

        self.__mask_images()

    def __mask_images(self) -> None:
        self.__first_mask = self.__create_mask(self.__first_image.raw_data_16bit())
        self.__second_mask = self.__create_mask(self.__second_image.raw_data_16bit())

    def __create_mask(self, image) -> numpy.ndarray:
        ret, threshold = cv2.threshold(image, 1, 0xFFFF, cv2.THRESH_BINARY_INV)
        return threshold

    def raw_data(self) -> numpy.ndarray:
        if self.__optical_flow is None:
            self.__compute_optical_flow()
        return self.__optical_flow

    def visual_data(self) -> numpy.ndarray:
        return self.__colored_optical_flow()

    def __compute_optical_flow(self) -> None:
        tik = time.process_time()
        masked_first_image = numpy.ma.masked_array(self.__first_image.raw_data_16bit(),
                                                   mask=self.__second_mask).filled(0)
        masked_second_image = numpy.ma.masked_array(self.__second_image.raw_data_16bit(),
                                                    mask=self.__first_mask).filled(0)

        self.__optical_flow = cv2.calcOpticalFlowFarneback(masked_first_image,
                                                           masked_second_image,
                                                           None, 0.5, 6, 15, 3, 5, 1.2, 0)
        tok = time.process_time()
        logger.success("Finished optical flow in {} seconds.".format(tok - tik))

    def __colored_optical_flow(self) -> numpy.ndarray:
        optical_flow = self.raw_data()
        magnitude, angle = cv2.cartToPolar(optical_flow[..., 0], optical_flow[..., 1])

        magnitude = numpy.ma.masked_array(magnitude, mask=self.__first_mask).filled(0)
        magnitude = numpy.ma.masked_array(magnitude, mask=self.__second_mask).filled(0)

        colored_clone = cv2.cvtColor(self.__first_image.raw_data_16bit(), cv2.COLOR_GRAY2BGR)
        hsv = numpy.zeros_like(colored_clone).astype(numpy.uint8)

        hsv[..., 0] = angle * 180 / numpy.pi / 2
        hsv[..., 1] = 255
        hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        hsv[..., 2] = self.scale_to_8bit(hsv[..., 2], 4)

        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return bgr

    @staticmethod
    def scale_to_8bit(image, value) -> numpy.ndarray:
        image32 = image.astype(numpy.int32)
        image32 = image32 * value
        numpy.clip(image32, 0, 255, out=image32)
        return image32.astype(numpy.uint8)

    def name(self) -> str:
        return self.NAME

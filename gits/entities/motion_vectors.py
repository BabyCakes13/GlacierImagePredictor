#!/usr/bin/env python3
import time
import cv2
import numpy

from entities.aligned.aligned_image import AlignedImage
from entities.image import Image
from utils import logging
from utils.utils import debug_trace
logger = logging.getLogger(__name__)


class MotionVectorsArrows():
    NAME = "Motion Vectors Arrows"
    def __init__(self, motionvectors, first_image: AlignedImage, second_image: AlignedImage):
        self.__first_image = first_image
        self.__second_image = second_image
        self.__motionvectors = motionvectors

    def clear(self):
        pass

    def name(self):
        return self.NAME

    def scene_name(self):
        return self.__motionvectors.scene_name()

    def visual_data(self) -> numpy.ndarray:
        return self.__arrowed_optical_flow()

    def raw_data(self) -> numpy.ndarray:
        pass

    def __create_mask(self, image) -> numpy.ndarray:
        ret, threshold = cv2.threshold(image, 1, 0xFFFF, cv2.THRESH_BINARY_INV)
        return threshold

    def __arrowed_optical_flow(self) -> numpy.ndarray:
        first_mask = self.__create_mask(self.__first_image.raw_data_16bit())
        second_mask = self.__create_mask(self.__second_image.raw_data_16bit())
        base_image = self.__second_image.visual_data()

        optical_flow = self.__motionvectors.raw_data()

        thiccness = 2
        step = 30

        for y in range(0, base_image.shape[0], step):
            for x in range(0, base_image.shape[1], step):
                if first_mask[y][x] == 0 and second_mask[y][x] == 0:
                    dx, dy = optical_flow[y][x]
                    end_point = (x, y)
                    start_point = (int(x - dx), int(y - dy))
                    color = (0, 0, 255)
                    cv2.arrowedLine(base_image, start_point, end_point, color, thiccness)

        return base_image


class MotionVectors(Image):

    NAME = "Motion Vectors Color"

    def __init__(self, first_image: AlignedImage, second_image: AlignedImage):
        self.__first_image = first_image
        self.__second_image = second_image
        self.__optical_flow = None

    def clear(self):
        self.__optical_flow = None

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

        first_mask = self.__create_mask(self.__first_image.raw_data_16bit())
        second_mask = self.__create_mask(self.__second_image.raw_data_16bit())
        masked_first_image = numpy.ma.masked_array(self.__first_image.raw_data_16bit(),
                                                   mask=second_mask).filled(0)
        masked_second_image = numpy.ma.masked_array(self.__second_image.raw_data_16bit(),
                                                    mask=first_mask).filled(0)

        self.__optical_flow = cv2.calcOpticalFlowFarneback(masked_first_image,
                                                           masked_second_image,
                                                           None,
                                                           pyr_scale=0.5,
                                                           levels=6,
                                                           winsize=15,
                                                           iterations=3,
                                                           poly_n=5,
                                                           poly_sigma=1.2,
                                                           flags=0)
        tok = time.process_time()
        logger.success("Finished optical flow in {} seconds.".format(tok - tik))

    def __colored_optical_flow(self) -> numpy.ndarray:
        first_mask = self.__create_mask(self.__first_image.raw_data_16bit())
        second_mask = self.__create_mask(self.__second_image.raw_data_16bit())

        optical_flow = self.raw_data()
        magnitude, angle = cv2.cartToPolar(optical_flow[..., 0], optical_flow[..., 1])

        magnitude = numpy.ma.masked_array(magnitude, mask=first_mask).filled(0)
        magnitude = numpy.ma.masked_array(magnitude, mask=second_mask).filled(0)

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

    def create_mask(self, image):
        ret, threshold = cv2.threshold(image, 1, 0xFFFF, cv2.THRESH_BINARY_INV)
        return threshold

    def scene_name(self):
        return self.__first_image.scene_name()

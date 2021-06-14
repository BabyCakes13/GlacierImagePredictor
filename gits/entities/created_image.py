#!/usr/bin/env python3
from scipy import signal
import numpy
import cv2

from utils.utils import debug_trace
from entities.image import Image
from utils import logging
logger = logging.getLogger(__name__)


class CreatedImage(Image):

    NAME = "Created Image"
    KERNEL_SIZE = 5

    def __init__(self, optical_flow, previous_image):
        self.__image = None
        self.__optical_flow = optical_flow
        self.__previous_image = previous_image
        self.__width, self.__height = self.__get_shape()
        self.__absolute_coordinates = None
        self.__kernel = self.__generate_kernel(5)

    def ndarray(self) -> numpy.ndarray:
        if self.__image is None:
            self.__generate_image()
            self.__zero_out_edges()
            self.__filter_by_average()
            self.__image = self.__image.astype(numpy.uint16)
        return self.__image

    def __generate_image(self) -> None:
        self.__image = numpy.zeros_like(self.__previous_image.ndarray()).astype(numpy.int16)
        self.__image -= 1
        self.__absolute_coodrinates = self.__generate_absolute_coordinates()

        self.__image[self.__absolute_coodrinates[..., 1],
                     self.__absolute_coodrinates[..., 0]] = self.__previous_image.ndarray() / 2

    def __generate_absolute_coordinates(self) -> numpy.ndarray:
        index_array = self.__generate_index_array()

        absolute_coordinates = self.__optical_flow.optical_flow() + index_array
        absolute_coordinates = absolute_coordinates.astype(numpy.int)
        absolute_coordinates[..., 0] = numpy.clip(absolute_coordinates[..., 0], 0,
                                                  self.__width - 1)
        absolute_coordinates[..., 1] = numpy.clip(absolute_coordinates[..., 1], 0,
                                                  self.__height - 1)
        return absolute_coordinates

    def __generate_index_array(self) -> numpy.ndarray:
        xarr = numpy.tile(numpy.arange(self.__width), (self.__height, 1))
        yarr = numpy.tile(numpy.arange(self.__height).reshape(self.__height, 1), (1, self.__width))

        index_array = numpy.zeros((self.__height, self.__width, 2))
        index_array[..., 0] = xarr
        index_array[..., 1] = yarr
        return index_array

    def __get_shape(self) -> tuple:
        height = self.__previous_image.ndarray().shape[0]
        width = self.__previous_image.ndarray().shape[1]
        logger.notice("Width ({}) and  height ({}) of the created image.".format(width, height))
        return width, height

    def __filter_by_average(self):
        zero_points = numpy.where(self.__image == -1)
        logger.notice("Zero points has {} elements.".format(len(zero_points)))
        zero_point_pairs = tuple(zip(*zero_points))
        len_zero_point_pairs = len(zero_point_pairs)

        count = 0
        for y, x in zero_point_pairs:
            if y < (self.__height - self.KERNEL_SIZE // 2) and y >= (self.KERNEL_SIZE // 2) and \
               x < (self.__width - self.KERNEL_SIZE // 2) and x >= (self.KERNEL_SIZE // 2):
                self.__image[y][x] = self.__average_pixel(y, x)
                count += 1

                if count % 10000 == 0:
                    logger.notice("Done {} and {}, remaining {} ".format(y, x, len_zero_point_pairs - count))

    def __average_pixel(self,  y, x):
        image_chunk = self.__image
        image_chunk = image_chunk[y - self.KERNEL_SIZE // 2:y + self.KERNEL_SIZE // 2 + 1,
                                  x - self.KERNEL_SIZE // 2:x + self.KERNEL_SIZE // 2 + 1]

        value = numpy.average(image_chunk, weights=self.__kernel)

        return value

    def __zero_out_edges(self) -> None:
        ret, mask = cv2.threshold(self.__previous_image.ndarray(), 1, 0xFFFF, cv2.THRESH_BINARY_INV)
        masked_image = numpy.ma.masked_array(self.__image, mask=mask).filled(0)
        self.__image = masked_image

    def __generate_kernel(self, kernel_size):
        kernel1d = signal.gaussian(kernel_size, std=kernel_size / 3).reshape(kernel_size, 1)
        kernel2d = numpy.outer(kernel1d, kernel1d)
        return kernel2d

    def name(self) -> str:
        return self.NAME

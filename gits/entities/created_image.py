#!/usr/bin/env python3
import numpy

from entities.image import Image

from utils.utils import debug_trace
from utils import logging
logger = logging.getLogger(__name__)


class CreatedImage(Image):

    NAME = "Created Image"

    def __init__(self, optical_flow, previous_image):
        self.__image = None
        self.__optical_flow = optical_flow
        self.__previous_image = previous_image
        self.__width, self.__height = self.__get_shape()
        self.__absolute_coordinates = None

    def ndarray(self) -> numpy.ndarray:
        if self.__image is None:
            self.__create_image()
        return self.__image

    def __create_image(self):
        self.__image = numpy.zeros_like(self.__previous_image.ndarray())
        self.__absolute_coodrinates = self.__generate_absolute_coordinates()

        for y in range(0, self.__height - 1):
            for x in range(0, self.__width - 1):
                self.__compute_pixel(x, y)
            logger.notice("Computed pixel on line {}".format(y))

    def __generate_absolute_coordinates(self) -> numpy.ndarray:
        xarr = numpy.tile(numpy.arange(self.__width), (self.__height, 1))
        yarr = numpy.tile(numpy.arange(self.__height).reshape(self.__height, 1), (1, self.__width))

        index_array = numpy.zeros((self.__height, self.__width, 2))
        index_array[..., 0] = xarr
        index_array[..., 1] = yarr

        debug_trace()

        absolute_coordinates = self.__optical_flow.optical_flow() + index_array
        absolute_coordinates = absolute_coordinates.astype(numpy.int)
        absolute_coordinates[..., 0] = numpy.clip(absolute_coordinates[..., 0], 0, self.__width - 1)
        absolute_coordinates[..., 1] = numpy.clip(absolute_coordinates[..., 1], 0, self.__height - 1)

        logger.notice("xarr: {}\nyarr: {}\nabsolute_coordinates{}".format(xarr, yarr, absolute_coordinates))

        return absolute_coordinates

    def __compute_pixel(self, x, y) -> None:
        image_x = self.__absolute_coodrinates[y][x][0]
        image_y = self.__absolute_coodrinates[y][x][1]
        self.__image[image_y][image_x] = self.__previous_image.ndarray()[y][x]

    def __get_shape(self) -> tuple():
        height = self.__previous_image.ndarray().shape[0]
        width = self.__previous_image.ndarray().shape[1]
        logger.notice("Width ({}); Height ({})".format(width, height))
        return width, height

    def name(self) -> str:
        return self.NAME

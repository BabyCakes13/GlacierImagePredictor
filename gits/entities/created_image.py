#!/usr/bin/env python3
import numpy

from entities.image import Image

from utils import logging
logger = logging.getLogger(__name__)


class CreatedImage(Image):

    NAME = "Created Image"

    def __init__(self, optical_flow, previous_image):
        self.__image = None
        self.__optical_flow = optical_flow
        self.__previous_image = previous_image
        self.__width, self.__height = self.__get_shape()

    def ndarray(self) -> numpy.ndarray:
        if self.__image is None:
            self.__create_image()
        return self.__image

    def __create_image(self):
        self.__allocate_image()

        for y in range(4000, 4250):
            for x in range(4000, 4250):
                self.__compute_pixel(x, y)
            logger.notice("Computed pixel on line {}".format(y))

    def __compute_pixel(self, x, y) -> None:
        movement_on_x = self.__optical_flow.ndarray()[y][x][0]
        movement_on_y = self.__optical_flow.ndarray()[y][x][1]

        moved_x = movement_on_x + x
        moved_y = movement_on_y + y

        if moved_x < 0 or moved_x >= self.__width:
            return
        if moved_y < 0 or moved_y >= self.__height:
            return
        self.__image[moved_y][moved_x] = self.__previous_image.ndarray()[y][x]

    def __allocate_image(self):
        self.__image = numpy.zeros_like(self.__previous_image.ndarray())

    def __get_shape(self) -> tuple():
        height = self.__previous_image.ndarray().shape[0]
        width = self.__previous_image.ndarray().shape[1]
        logger.notice("Width ({}); Height ({})".format(width, height))
        return width, height

    def name(self) -> str:
        return self.NAME

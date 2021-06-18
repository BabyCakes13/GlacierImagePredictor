#!/usr/bin/env python3
import time
import numpy
import cv2
import multiprocessing
from multiprocessing import shared_memory

from entities.image import Image
from utils.utils import progress, debug_trace
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
        self.__kernel = self.__generate_kernel()

        self.__finished = 0
        self.__total_zero_points = 0

    def __get_shape(self) -> tuple:
        height = self.__previous_image.ndarray().shape[0]
        width = self.__previous_image.ndarray().shape[1]
        logger.notice("Width ({}) and  height ({}) of the created image.".format(width, height))
        return width, height

    def __generate_kernel(self) -> numpy.ndarray:
        kernel1d = [abs(abs((self.KERNEL_SIZE+1)//2 - x) - (self.KERNEL_SIZE+1)//2)
                    for x in range(1, self.KERNEL_SIZE+1)]
        kernel2d = numpy.outer(kernel1d, kernel1d)
        kernel2d[self.KERNEL_SIZE // 2][self.KERNEL_SIZE // 2] = 0
        return kernel2d

    def ndarray(self) -> numpy.ndarray:
        if self.__image is None:
            self.__create_image()
        return self.__image

    def __create_image(self) -> numpy.ndarray:
        self.__initialise_image()
        self.__generate_image_based_on_movement()
        self.__mask_image()
        self.__filter_by_average()
        self.__image = self.__image.astype(numpy.uint16) * 2

    def __initialise_image(self) -> None:
        self.__image = numpy.zeros_like(self.__previous_image.ndarray()).astype(numpy.int16)
        self.__image -= 1

    def __generate_image_based_on_movement(self) -> None:
        logger.notice("Generating image...")
        absolute_coodrinates = self.__generate_absolute_coordinates()
        self.__image[absolute_coodrinates[..., 1],
                     absolute_coodrinates[..., 0]] = self.__previous_image.ndarray() / 2

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

    def __mask_image(self) -> None:
        logger.notice("Masking image...")
        ret, mask = cv2.threshold(self.__previous_image.ndarray(), 1, 0xFFFF, cv2.THRESH_BINARY_INV)
        masked_image = numpy.ma.masked_array(self.__image, mask=mask).filled(0)
        self.__image = masked_image

        logger.success("Finished masking image.")

    def __filter_by_average(self) -> None:
        tic = time.process_time()
        cores = multiprocessing.cpu_count()
        logger.notice("Filtering by average on {} cores...".format(cores))

        zero_points = numpy.where(self.__image == -1)
        zero_point_pairs = tuple(zip(*zero_points))
        self.__total_zero_points = len(zero_point_pairs)

        shm = shared_memory.SharedMemory(create=True, size=self.__image.nbytes)
        shm_image = numpy.ndarray(self.__image.shape, dtype=self.__image.dtype, buffer=shm.buf)
        shm_image[:][:] = self.__image[:][:]

        with multiprocessing.Pool(processes=cores) as executor:
            executor.map(filter_pixel, [(point, shm,
                                         self.__image.shape,
                                         self.__image.dtype,
                                         self.__height,
                                         self.__width,
                                         self.KERNEL_SIZE) for point in zero_point_pairs])

        self.__image[:][:] = shm_image[:][:]
        shm.close()
        shm.unlink()

        tok = time.process_time()
        logger.success("Finished filtering in {}".format(tok - tic))

    def _filter_pixel_by_average(self, pixel):
        y, x = pixel
        if self.__point_inside_boundary(y, x):
            self.__image[y][x] = self.__average_pixel(y, x)
            self.__finished += 1
            if self.__finished % 10000 == 0:
                progress(self.__finished, self.__total_zero_points, "Finished generating image.")

    def __point_inside_boundary(self, y, x) -> bool:
        if y < (self.__height - self.KERNEL_SIZE // 2) and y >= (self.KERNEL_SIZE // 2) and \
           x < (self.__width - self.KERNEL_SIZE // 2) and x >= (self.KERNEL_SIZE // 2):
            return True
        return False

    def __average_pixel(self,  y, x) -> int:
        image_chunk = self.__image
        image_chunk = image_chunk[y - self.KERNEL_SIZE // 2:y + self.KERNEL_SIZE // 2 + 1,
                                  x - self.KERNEL_SIZE // 2:x + self.KERNEL_SIZE // 2 + 1]
        kernel = self.__remove_weight_for_number(image_chunk, self.__kernel, 0)
        kernel = self.__remove_weight_for_number(image_chunk, kernel, -1)

        weights_sum = numpy.sum(kernel)
        if weights_sum == 0:
            return 0
        nominator = numpy.sum(image_chunk * kernel)
        value = nominator // weights_sum

        return value

    def __remove_weight_for_number(self, image_chunk, kernel, number) -> numpy.ndarray:
        number_coordinates = numpy.where(image_chunk == number)
        kernel_without_weight = numpy.copy(kernel)
        kernel_without_weight[number_coordinates[0], number_coordinates[1]] = 0
        return kernel_without_weight

    def name(self) -> str:
        return self.NAME


def filter_pixel(arg):
    point, shm, shape, dtype, height, width, kernel_size = arg
    shm_image = numpy.ndarray(shape, dtype, buffer=shm.buf)

    y, x = point
    if y < (height - kernel_size // 2) and y >= (kernel_size // 2) and \
       x < (width - kernel_size // 2) and x >= (kernel_size // 2):
        image_chunk = shm_image
        image_chunk = image_chunk[y - kernel_size // 2:y + kernel_size // 2 + 1,
                                  x - kernel_size // 2:x + kernel_size // 2 + 1]

        kernel1d = [abs(abs((kernel_size+1)//2 - x) - (kernel_size+1)//2)
                    for x in range(1, kernel_size+1)]
        kernel = numpy.outer(kernel1d, kernel1d)
        kernel[kernel_size // 2][kernel_size // 2] = 0

        zero_coordinates = numpy.where(image_chunk == 0)
        kernel[zero_coordinates[0], zero_coordinates[1]] = 0
        minus_one_coordinates = numpy.where(image_chunk == -1)
        kernel[minus_one_coordinates[0], minus_one_coordinates[1]] = 0

        weights_sum = numpy.sum(kernel)
        if weights_sum == 0:
            return 0
        nominator = numpy.sum(image_chunk * kernel)
        value = nominator // weights_sum
        shm_image[y][x] = value

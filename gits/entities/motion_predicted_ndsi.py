#!/usr/bin/env python3
import os
import time
import numpy
import tifffile
import multiprocessing
from multiprocessing import shared_memory

from entities.ndsi import NDSI
from entities.motion_vectors import MotionVectors
from utils import logging
logger = logging.getLogger(__name__)


class MotionPredictedNDSI(NDSI):

    NAME = "Motion Predicted NDSI"
    KERNEL_SIZE = 5

    INITIAL_VALUE = -1234

    def __init__(self, motion_vectors: MotionVectors, previous_image: NDSI):
        self.__image = None
        self.__motion_vectors = motion_vectors
        self.__previous_image = previous_image
        self.__w, self.__h = None, None
        self.__kernel = self.__generate_kernel()

        self.__finished = 0
        self.__total_zero_points = 0

    def clear(self):
        self.__image = None

    def name(self) -> str:
        return self.NAME

    def scene_name(self):
        return self.__previous_image.scene_name()

    @property
    def __width(self):
        if self.__w is None:
            self.__w, self.__h = self.__get_shape()

        return self.__w

    @property
    def __height(self):
        if self.__h is None:
            self.__h, self.__h = self.__get_shape()

        return self.__h

    def __get_shape(self) -> tuple:
        height = self.__previous_image.raw_data().shape[0]
        width = self.__previous_image.raw_data().shape[1]
        logger.notice("Width ({}) and  height ({}) of the created image.".format(width, height))
        return width, height

    def __generate_kernel(self) -> numpy.ndarray:
        kernel1d = [abs(abs((self.KERNEL_SIZE+1)//2 - x) - (self.KERNEL_SIZE+1)//2)
                    for x in range(1, self.KERNEL_SIZE+1)]
        kernel2d = numpy.outer(kernel1d, kernel1d)
        kernel2d[self.KERNEL_SIZE // 2][self.KERNEL_SIZE // 2] = 0
        return kernel2d

    def raw_data(self) -> numpy.ndarray:
        if self.__image is None:
            path = self.__previous_image.create_band_path(suffix="_PREDICTED_CACHED")
            logger.info(path)

            if os.path.exists(path):
                logger.notice("Read cached file: " + path)
                self.__image = tifffile.imread(path)
            else:
                self.__create_image()
                logger.notice("Write cached file: " + path)
                tifffile.imwrite(path, self.__image)

        return self.__image

    def __create_image(self) -> numpy.ndarray:
        self.__initialise_image()
        self.__generate_image_based_on_movement()
        self.__mask_image()
        self.__filter_by_average()

    def __initialise_image(self) -> None:
        previous_image = self.__previous_image.raw_data()
        self.__image = numpy.full_like(previous_image, MotionPredictedNDSI.INITIAL_VALUE)

    def __generate_image_based_on_movement(self) -> None:
        tic = time.process_time()
        logger.notice("Generating image...")
        absolute_coordinates = self.__generate_absolute_coordinates()
        self.__image[absolute_coordinates[..., 1],
                     absolute_coordinates[..., 0]] = self.__previous_image.raw_data()
        tok = time.process_time()
        logger.success("Finished generating the initial image in {}".format(tok - tic))

    def __generate_absolute_coordinates(self) -> numpy.ndarray:
        index_array = self.__generate_index_array()

        absolute_coordinates = self.__motion_vectors.raw_data() + index_array
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
        previous_image = self.__previous_image.raw_data()

        mask = numpy.copy(previous_image)

        mask[mask == mask] = 0
        mask[mask != mask] = 1

        masked_image = numpy.ma.masked_array(self.__image, mask=mask).filled(numpy.nan)
        self.__image = masked_image

        logger.success("Finished masking image.")

    def __filter_by_average(self) -> None:
        tic = time.process_time()
        cores = multiprocessing.cpu_count()
        logger.notice("Filtering by average on {} cores...".format(cores))

        zero_points = numpy.where(self.__image == MotionPredictedNDSI.INITIAL_VALUE)
        zero_point_pairs = tuple(zip(*zero_points))
        self.__total_zero_points = len(zero_point_pairs)

        shm = shared_memory.SharedMemory(create=True, size=self.__image.nbytes)
        shm_image = numpy.ndarray(self.__image.shape, dtype=self.__image.dtype, buffer=shm.buf)
        shm_image[:][:] = self.__image[:][:]

        self.__finished = multiprocessing.Value('i', 0)

        with multiprocessing.Pool(processes=cores) as executor:
            executor.map(MotionPredictedNDSI.filter_pixel,
                         [(point, shm,
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

    def filter_pixel(arg):
        point, shm, shape, dtype, height, width, kernel_size = arg
        shm_image = numpy.ndarray(shape, dtype, buffer=shm.buf)

        y, x = point
        if MotionPredictedNDSI.__point_inside_boundary(kernel_size, width, height, y, x):

            image_chunk = shm_image
            image_chunk = image_chunk[y - kernel_size // 2:y + kernel_size // 2 + 1,
                                      x - kernel_size // 2:x + kernel_size // 2 + 1]

            kernel1d = [abs(abs((kernel_size+1)//2 - x) - (kernel_size+1)//2)
                        for x in range(1, kernel_size+1)]
            kernel = numpy.outer(kernel1d, kernel1d)
            kernel[kernel_size // 2][kernel_size // 2] = 0

            zero_coordinates = numpy.where(image_chunk != image_chunk)
            kernel[zero_coordinates[0], zero_coordinates[1]] = 0
            minus_one_coordinates = numpy.where(image_chunk == MotionPredictedNDSI.INITIAL_VALUE)
            kernel[minus_one_coordinates[0], minus_one_coordinates[1]] = 0

            image_chunk[image_chunk != image_chunk] = 0

            weights_sum = numpy.sum(kernel)
            if weights_sum == 0:
                return NDSI.VALUE_INTERVAL[0]
            nominator = numpy.sum(image_chunk * kernel)
            value = nominator / weights_sum
            shm_image[y][x] = value

    def __point_inside_boundary(KERNEL_SIZE, width, height, y, x) -> bool:
        if y < (height - KERNEL_SIZE // 2) and y >= (KERNEL_SIZE // 2) and \
           x < (width - KERNEL_SIZE // 2) and x >= (KERNEL_SIZE // 2):
            return True
        return False


class MotionPredictedNDSIOverlay():
    NAME = "Motion Predicted Overlay NDSI"

    def __init__(self, predicted_ndsi, previous_ndsi):
        self.__predicted_ndsi = predicted_ndsi
        self.__previous_ndsi = previous_ndsi

    def clear(self):
        pass

    def name(self):
        return self.NAME

    def scene_name(self):
        return self.__predicted_ndsi.scene_name()

    def visual_data(self):
        old_ndsi = self.__previous_ndsi.visual_data()
        predicted_ndsi_colored = self.__predicted_ndsi.visual_data()

        predicted_ndsi_colored[..., 0] = old_ndsi[..., 0]

        return predicted_ndsi_colored

    def raw_data(self) -> numpy.ndarray:
        pass

    def snow_percentage(self):
        return self.__predicted_ndsi.snow_percentage()

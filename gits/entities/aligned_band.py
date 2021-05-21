#!/usr/bin/env python3
from entities.aligned_image import AlignedImage


from utils import logging
logger = logging.getLogger(__name__)


class AlignedBand(AlignedImage):
    def __init__(self, band, reference_band):
        AlignedImage.__init__(self, band, reference_band)
        self.__band = band

    def name(self):
        return self.__band.name()

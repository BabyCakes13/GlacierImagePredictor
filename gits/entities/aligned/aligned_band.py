#!/usr/bin/env python3
from entities.aligned.aligned_image import AlignedImage
from entities.band import Band

from utils import logging
logger = logging.getLogger(__name__)


class AlignedBand(AlignedImage):
    def __init__(self, band: Band, reference_band: Band):
        AlignedImage.__init__(self, band, reference_band)
        self.__band = band

    def name(self):
        return self.__band.name()

    def band(self) -> Band:
        return self.__band

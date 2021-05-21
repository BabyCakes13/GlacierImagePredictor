#!/usr/bin/env python3
from entities.aligned_image import AlignedImage


from utils import logging
logger = logging.getLogger(__name__)


class AlignedBand(AlignedImage):
    def __init__(self, band):
        AlignedImage.__init__(self, band)
        self._band = band

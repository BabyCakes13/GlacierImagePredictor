#!/usr/bin/env python3
from entities.aligned_image import AlignedImage
from entities.true_color import TrueColor


class AlignedTrueColor(AlignedImage):
    def __init__(self, true_color: TrueColor):
        AlignedImage.__init__(self, true_color)
        self.__true_color = true_color

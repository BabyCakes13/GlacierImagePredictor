#!/usr/bin/env python3
from entities.aligned.aligned_image import AlignedImage
from entities.true_color import TrueColor


class AlignedTrueColor(AlignedImage):
    def __init__(self, true_color: TrueColor, reference):
        AlignedImage.__init__(self, true_color, reference)
        self.__true_color = true_color

    def name(self):
        return self.__true_color.name()

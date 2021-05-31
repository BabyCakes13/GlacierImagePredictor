#!/usr/bin/env python3
class Alignment:
    def __init__(self, image, reference):
        self.__image = image
        self.__reference = reference

    def normalise(self, image):

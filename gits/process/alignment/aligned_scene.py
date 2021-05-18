#!/usr/bin/env python3
from entities.scene_interface import SceneInterface


class AlignedScene(SceneInterface):
    def __init__(self, reference_scene, scene):
        SceneInterface.__init__(self)

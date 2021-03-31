from process.entities.scene import Scene


class RegionOfInterest:
    def __init__(self, wgi_path: int, wgi_row: int):
        """
        Constructor of the RegionOfInterest class.

        :param wgi_path: https://landsat.gsfc.nasa.gov/about/worldwide-reference-system
        :param wgi_row: https://landsat.gsfc.nasa.gov/about/worldwide-reference-system
        """
        self.__wgi_path = wgi_path
        self.__wgi_row = wgi_row

        self.__scenes = []

    def wgi_path(self):
        return self.__wgi_path

    def wgi_row(self):
        return self.__wgi_row

    def add_scene(self, scene: Scene) -> None:
        self.__scenes.append(scene)

    def print_scenes(self) -> None:
        for scene in self.__scenes:
            print(scene)

    def __str__(self):
        return "RegionOfInterest[{}, {}]".format(self.__wgi_path, self.__wgi_row)

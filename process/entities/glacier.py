class Glacier:
    def __init__(self, wgi_id):
        self.__wgi_id = wgi_id

        # Region of Interests representing different path row pairs.
        self.__rois = []

    def set_rois(self, rois: list) -> None:
        self.__rois = rois

    def rois(self) -> list:
        return self.__rois

    def wgi_id(self) -> str:
        return self.__wgi_id

    def __str__(self):
        return "Glacier[{}]".format(self.__wgi_id)

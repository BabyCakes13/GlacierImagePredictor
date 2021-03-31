from process.entities.roi import RegionOfInterest


class Glacier:
    def __init__(self, wgi_id):
        self.__wgi_id = wgi_id

        # Region of Interests representing different path row pairs.
        self.__rois = []

    def add_roi(self, roi: RegionOfInterest) -> None:
        self.__rois.append(roi)

    def __str__(self):
        return "Glacier[{}]".format(self.__wgi_id)

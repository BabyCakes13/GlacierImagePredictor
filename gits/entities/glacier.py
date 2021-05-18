from utils import logging
logger = logging.getLogger(__name__)


class Glacier:
    def __init__(self, wgi_id):
        self.__wgi_id = wgi_id

        # Region of Interests representing different path row pairs.
        self.__rois = []

        logger.debug("Created {}.".format(self.__str__()))

    def set_rois(self, rois: list) -> None:
        self.__rois = rois

    def rois(self) -> list:
        return self.__rois

    def wgi_id(self) -> str:
        return self.__wgi_id

    def __str__(self):
        return "Glacier[{}]".format(self.__wgi_id)


def find_glacier_by_wgi_id(glacier_wgi_id: str, glaciers: list) -> Glacier:
    for glacier in glaciers:
        if glacier.wgi_id() == glacier_wgi_id:
            return glacier
    return None


def get_wgi_id_list_from(glaciers: list) -> list:
    return [glacier.wgi_id() for glacier in glaciers]

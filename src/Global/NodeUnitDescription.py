#
#
#
import logging


class NodeUnitDescription(object):
    def __init__(self, node_id: str):
        self.__logger: logging.Logger = logging.getLogger("NodeDescriptionEntity-logger")
        self.__node_id: str = node_id
        self.__logger.debug(f"Created NodeDescriptionEntity with id {self.__node_id}")

    def get_node_id(self) -> str:
        self.__logger.debug(f"Created NodeDescriptionEntity -> get_node_id {self.__node_id}")
        return self.__node_id

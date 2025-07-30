#
#
#
import logging
from Global.NodeUnitDescription import NodeUnitDescription


class SupportNodeUnitDescriptionGenerator(object):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("NodeUnitIterator-logger")

    def get_entity(self, node_id: str) -> NodeUnitDescription:
        self.__logger.debug(f"SupportNodeUnitDescriptionGenerator: str with id {node_id}")
        node_description_entity_instance: NodeUnitDescription = NodeUnitDescription(
            node_id=node_id
        )
        self.__logger.debug(f"SupportNodeUnitDescriptionGenerator: str converted to NodeDescriptionEntity "
                            f"with id {node_description_entity_instance.get_node_id()}")
        return node_description_entity_instance

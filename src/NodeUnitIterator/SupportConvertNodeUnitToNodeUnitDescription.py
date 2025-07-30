#
#
#
import logging
from Global2p1.NodeUnit import NodeUnit
from Global.NodeUnitDescription import NodeUnitDescription


class SupportConvertNodeUnitToNodeUnitDescription(object):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("NodeUnitIterator-logger")

    def get_entity(self, dto_node_unit: NodeUnit) -> NodeUnitDescription:
        self.__logger.debug(f"SupportConvertNodeUnitToNodeUnitDescription: DtoNodeUnit with id {dto_node_unit.get_node_id()}")
        node_id: str = dto_node_unit.get_node_id()
        node_description_entity_instance: NodeUnitDescription = NodeUnitDescription(
            node_id=node_id
        )
        self.__logger.debug(f"SupportConvertNodeUnitToNodeUnitDescription: DtoNodeUnit converted to NodeDescriptionEntity "
                            f"with id {node_description_entity_instance.get_node_id()}")
        return node_description_entity_instance

#
#
#
import logging
from typing import Union
from Global.InterfaceNodeUnitIterator import InterfaceNodeUnitIterator

from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository

from Global2p1.NodeUnit import NodeUnit
from typing import Optional

from .RecursiveDescriptionsSequenceGenerator import RecursiveDescriptionsSequenceGenerator
from Global.NodeUnitDescription import NodeUnitDescription
from src.LibByzaticCommon import Exceptions


class NodeUnitIterator(InterfaceNodeUnitIterator):
    def __init__(self, node_unit_repository: InterfaceNodeUnitRepository, root_node_description: Optional[NodeUnitDescription] = None) -> None:
        self.__logger: logging.Logger = logging.getLogger("NodeUnitIterator-logger")
        self.__RootNodeDescription: Optional[NodeUnitDescription] = root_node_description
        self.__NodeUnitRepository: InterfaceNodeUnitRepository = node_unit_repository
        self.__RecursiveDescriptionsSequenceGenerator: RecursiveDescriptionsSequenceGenerator = RecursiveDescriptionsSequenceGenerator(self.__NodeUnitRepository)
        self.__descriptions_sequence: list[NodeUnitDescription] = []
        self.__descriptions_sequence_index_limit: int = 0
        try:
            self.__create_descriptions_sequence()
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)
        self.__set_descriptions_sequence_index_limit()
        # self.__reverse_description_sequence()
        self.__pointer: int = 0

    def has_next(self) -> bool:
        if self.__pointer <= self.__descriptions_sequence_index_limit:
            return True
        else:
            return False

    def get_next(self) -> Union[NodeUnitDescription, None]:
        try:
            if self.__pointer > self.__descriptions_sequence_index_limit:
                return None
            else:
                self.__logger.debug(f"GraphIterator: get {self.__pointer + 1} of {self.__descriptions_sequence_index_limit + 1}")
                description_item: NodeUnitDescription = self.__descriptions_sequence[self.__pointer]
                self.__pointer = self.__pointer + 1
                return description_item
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)

    def __create_descriptions_sequence(self) -> None:
        try:
            self.__logger.debug(f"Try to create descriptions sequence")
            root_node: NodeUnit
            if self.__RootNodeDescription is None:
                self.__logger.debug(f"root node description is not defined, using internal searching for root node")
                root_node = self.__NodeUnitRepository.get_root_node_unit()
            else:
                self.__logger.debug(f"root node description is defined, id {self.__RootNodeDescription.get_node_id()}")
                root_node = self.__NodeUnitRepository.get_node_unit(self.__RootNodeDescription)
            self.__logger.debug(f"Found root node with id {root_node.get_node_id()}")
            self.__logger.debug(f"Recursive Descriptions Sequence Generation begging")
            self.__descriptions_sequence = self.__RecursiveDescriptionsSequenceGenerator.get_descriptions_sequence(root_node)
            self.__logger.debug(f"Recursive Descriptions Sequence Generation finished, descriptions sequence ready")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)

    def __set_descriptions_sequence_index_limit(self):
        self.__logger.debug(f"Len of descriptions sequence: {len(self.__descriptions_sequence)}")
        self.__descriptions_sequence_index_limit: int = len(self.__descriptions_sequence) - 1

    def __reverse_description_sequence(self) -> None:
        self.__descriptions_sequence.reverse()

    def reset(self) -> None:
        self.__pointer = 0
        self.__logger.debug(f"pointer was reset")



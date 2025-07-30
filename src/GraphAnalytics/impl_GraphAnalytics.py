#
#
#
import logging

from copy import deepcopy

from Global2p3.i_GraphAnalytics import i_GraphAnalytics

from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.InterfaceNodeUnitDescriptionIdRepository import InterfaceNodeUnitDescriptionIdRepository
from Global2p1.NodeUnit.NodeUnit import NodeUnit

from .SupportConvertNodeUnitToNodeUnitDescription import SupportConvertNodeUnitToNodeUnitDescription

from LibByzaticCommon import Exceptions


class impl_GraphAnalytics(i_GraphAnalytics):

    def __init__(self, node_unit_repository: InterfaceNodeUnitRepository):
        self.__logger: logging.Logger = logging.getLogger(f"GraphAnalytics-logger")
        self.__NodeUnitRepository: InterfaceNodeUnitRepository = node_unit_repository
        self.__NodeUnitDescriptionIdRepository: InterfaceNodeUnitDescriptionIdRepository = node_unit_repository
        self.__SupportConvertNodeUnitToNodeUnitDescription: SupportConvertNodeUnitToNodeUnitDescription = SupportConvertNodeUnitToNodeUnitDescription()

    def get_path_from_source_node_to_root_node(self, source_node_description: NodeUnitDescription, root_node_description: NodeUnitDescription) -> list[NodeUnitDescription]:
        try:
            path_to_vertex_of_graph_list: list[NodeUnitDescription] = []
            self.__from_source_node_to_root_node_loop(source_node_description, root_node_description, path_to_vertex_of_graph_list)
            return path_to_vertex_of_graph_list
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def reverse_path(self, list_node_unit_descriptions: list[NodeUnitDescription]) -> list[NodeUnitDescription]:
        try:
            list_node_unit_descriptions.reverse()
            inverted_list_node_unit_descriptions: list[NodeUnitDescription] = deepcopy(list_node_unit_descriptions)
            return inverted_list_node_unit_descriptions
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __from_source_node_to_root_node_loop(self, source_node_description: NodeUnitDescription, root_node_description: NodeUnitDescription, path_from_source_node_to_root_node: list[NodeUnitDescription]):
        path_from_source_node_to_root_node.append(source_node_description)
        if root_node_description.get_node_id() != source_node_description.get_node_id():
            source_node_unit: NodeUnit = self.__NodeUnitRepository.get_node_unit(source_node_description)
            source_node_unit_upstream: list[str] = source_node_unit.get_upstream()
            if len(source_node_unit_upstream) == 1:
                source_node_unit_upstream_item_description: NodeUnitDescription = self.__NodeUnitDescriptionIdRepository.get_node_unit_description_by_id(source_node_unit_upstream[0])
                self.__from_source_node_to_root_node_loop(source_node_unit_upstream_item_description, root_node_description, path_from_source_node_to_root_node)
            else:
                raise Exceptions.OperationIncompleteException(f"Everything you call life is imperfect, this algorithm too, sorry; "
                                                              f"Upstream shouldn't contains more then one node")
        else:
            pass


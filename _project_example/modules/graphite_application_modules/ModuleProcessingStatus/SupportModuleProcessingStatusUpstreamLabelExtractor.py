#
#
#
import logging

from ServicePrometheus.i_WorkerContext import i_WorkerContext
from Global2p3.i_GraphAnalytics import i_GraphAnalytics
from LibByzaticCommon import Exceptions

from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.NodeUnit.NodeUnit import NodeUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageInfo import NodeUnitWorkersPipelineStagesDescriptionStageInfo
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageData import NodeUnitWorkersPipelineStagesDescriptionStageData
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit


class SupportModuleProcessingStatusUpstreamLabelExtractor(object):
    def __init__(self, worker_context: i_WorkerContext, current_node_description: NodeUnitDescription, graph_analytics: i_GraphAnalytics):
        self.__logger: logging.Logger = logging.getLogger("Workers-ProcessingStatus-logger")
        self.__WorkerContext: i_WorkerContext = worker_context
        self.__current_node_description: NodeUnitDescription = current_node_description
        self.__GraphAnalytics: i_GraphAnalytics = graph_analytics

    def get_list_of_labels_in_upstream_chain_of_node_sequence(self):
        try:
            list_of_labels_in_upstream_chain_of_node_sequence: list[str] = []
            path_from_source_node_to_root_node: list[NodeUnitDescription] = self.__GraphAnalytics.get_path_from_source_node_to_root_node(self.__current_node_description, self.__WorkerContext.getRootNodeUnitDescription())
            reversed_path_from_source_node_to_root_node: list[NodeUnitDescription] = self.__GraphAnalytics.reverse_path(path_from_source_node_to_root_node)
            for path_item in reversed_path_from_source_node_to_root_node:
                node_unit: NodeUnit = self.__WorkerContext.getNodeUnitRepository().get_node_unit(path_item)
                self.__extract_labels(node_unit, list_of_labels_in_upstream_chain_of_node_sequence)
            return list_of_labels_in_upstream_chain_of_node_sequence
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __extract_labels(self, node_unit: NodeUnit, list_of_labels_in_upstream_chain_of_node_sequence: list[str]) -> None:
        self.__logger.debug(f"extracting labels from node with id {node_unit.get_node_id()}")

        stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo] = node_unit.get_workers_pipeline().get_stages_description().get_stages_info()
        for stages_info in stages_info_list:
                stage_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageData] = stages_info.get_stage_data()
                for stage_data in stage_data_list:
                    if stage_data.get_name() == "ModuleProcessingStatus":
                        self.__logger.debug(f"found module ModuleProcessingStatus in node with id {node_unit.get_node_id()}")
                        abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = stage_data.get_abstract_data_list()
                        for abstract_data in abstract_data_list:
                            if abstract_data.get_abstract_data_type() == "OutputDataLabel":
                                self.__logger.debug(f"found abstract_data OutputDataLabel with value {abstract_data.get_abstract_data_value()} in node with id {node_unit.get_node_id()}")
                                list_of_labels_in_upstream_chain_of_node_sequence.append(abstract_data.get_abstract_data_value())

        self.__logger.debug(f"extracting labels from node with id {node_unit.get_node_id()} complete")




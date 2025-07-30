#
#
#
import logging
from Global.InterfaceModuleManager import InterfaceModuleManager
from Global.NodeUnitDescription import NodeUnitDescription
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageData import NodeUnitWorkersPipelineStagesDescriptionStageData
from Global2p1.InterfaceNodeUnitRepository import InterfaceNodeUnitRepository
from Global2p1.NodeUnit.NodeUnit import NodeUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipeline import NodeUnitWorkersPipeline
from WorkersManager.local_api.i_PiplineManager import i_PiplineManager
from WorkersManager.impl_PiplineManager import impl_PiplineManager
from Global2p2.i_WorkersRepository import i_WorkersRepository
from Global2p2.i_Worker import i_Worker
from LibByzaticCommon import Exceptions


class impl_WorkersManager(InterfaceModuleManager):
    def __init__(self, node_unit_repository: InterfaceNodeUnitRepository, workers_repository: i_WorkersRepository) -> None:
        self.__logger: logging.Logger = logging.getLogger("WorkersManager-logger")
        self.__NodeUnitRepository: InterfaceNodeUnitRepository = node_unit_repository
        self.__PiplineManager: i_PiplineManager = impl_PiplineManager()
        self.__WorkersRepository: i_WorkersRepository = workers_repository

    def process_pipline(self, node_unit_description: NodeUnitDescription) -> None:
        try:
            self.__logger.debug(f"Running Workers Manager pipline processing for node unit description with id {node_unit_description.get_node_id()}")
            node_unit: NodeUnit = self.__NodeUnitRepository.get_node_unit(node_unit_description)
            self.__logger.debug(f"by description with id {node_unit_description.get_node_id()} received node unit with id {node_unit.get_node_id()}")
            workers_pipeline: NodeUnitWorkersPipeline = node_unit.get_workers_pipeline()
            self.__logger.debug(f"WorkersPipeline extracted from node unit with id {node_unit.get_node_id()}")
            self.__logger.debug(f"Call PiplineManager to generate pipline")
            sorted_pipline_stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageData] = self.__PiplineManager.make_pipline(workers_pipeline)
            self.__logger.debug(f"Finish PiplineManager")
            for sorted_pipline_stages_info_instance in sorted_pipline_stages_info_list:
                self.__logger.debug(f"Call WorkersRepository to get worker")
                worker_instance: i_Worker.WorkerMain = self.__WorkersRepository.get_worker(sorted_pipline_stages_info_instance, node_unit_description)
                self.__logger.debug(f"worker received")
                self.__logger.debug(f"execute worker")
                worker_instance.execute()
                self.__logger.debug(f"worker execution complete")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

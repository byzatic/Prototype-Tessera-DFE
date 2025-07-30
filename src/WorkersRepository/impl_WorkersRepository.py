#
#
#
import logging
from Global2p2.i_WorkersRepository import i_WorkersRepository
from Global2p2.i_Worker import i_Worker
from Global2p2.WorkerSpecification.WorkerSpecification import WorkerSpecification
# from Global2p2.WorkerSpecification.WorkerSpecificationDefaultOption import WorkerSpecificationDefaultOption
from Global2p2.i_DaoWorkersSpecifications import i_DaoWorkersSpecifications
from Global2p2.i_DaoWorkers import i_DaoWorkers
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageData import NodeUnitWorkersPipelineStagesDescriptionStageData
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceStorages import NodeUnitWorkersPipelineStagesGlobalSpaceStorages
from LibByzaticCommon import Exceptions
from Global2p2.i_StorageManager import i_StorageManager
from StorageManager.impl_StorageManager import impl_StorageManager
from ServicePrometheus.impl_WorkerContext import impl_WorkerContext
from Global.NodeUnitDescription import NodeUnitDescription


class impl_WorkersRepository(i_WorkersRepository):

    def __init__(self, dao_workers: i_DaoWorkers, dao_workers_specifications: i_DaoWorkersSpecifications, storage_manager: i_StorageManager):
        self.__logger: logging.Logger = logging.getLogger("WorkersRepository-logger")
        self.__DaoWorkers: i_DaoWorkers = dao_workers
        self.__DaoWorkersSpecifications: i_DaoWorkersSpecifications = dao_workers_specifications
        self.__StorageManager: i_StorageManager = storage_manager

    def get_worker(self, worker_stage_data: NodeUnitWorkersPipelineStagesDescriptionStageData, current_node_unit_description: NodeUnitDescription) -> i_Worker.WorkerMain:
        try:
            self.__logger.debug(f"Try to get worker from WorkersRepository")
            worker_name: str = worker_stage_data.get_name()
            self.__logger.debug(f"worker name: {worker_name}")
            worker_abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = worker_stage_data.get_abstract_data_list()
            self.__logger.debug(f"extracted worker parameters list")
            worker_configurations_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = worker_stage_data.get_configuration()
            self.__logger.debug(f"extracted worker configurations list")
            worker_specification: WorkerSpecification = self.__DaoWorkersSpecifications.get_worker_specification(worker_name)
            worker_module: i_Worker = self.__DaoWorkers.get_worker(worker_specification)
            worker_instance: i_Worker.WorkerMain = worker_module.WorkerMain(
                abstract_data_list=worker_abstract_data_list,
                configuration_list=worker_configurations_list,
                application_context=impl_WorkerContext(),
                current_node_description=current_node_unit_description
            )
            return worker_instance
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

#
#
#
import logging
from src.Global2p2.i_Worker import i_Worker
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from Global.NodeUnitDescription import NodeUnitDescription
from .ModuleProcess import ModuleProcess
from ServicePrometheus.i_WorkerContext import i_WorkerContext
from LibByzaticCommon import Exceptions


class WorkerMain(i_Worker.WorkerMain):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-PrometheusGetData-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self.__ModuleProcess: ModuleProcess = ModuleProcess(
            abstract_data_list=self._abstract_data_list,
            configuration_list=self._configuration_list,
            application_context=self._application_context,
            current_node_description=self._current_node_description
        )
        self.__module_version: str = "v1.0.0"

    def execute(self) -> None:
        try:
            self.__logger.debug(f"Module PrometheusGetData version {self.__module_version}")
            self.__logger.debug(f"START -> PrometheusGetData")
            self.__ModuleProcess.run()
            self.__logger.debug(f"FINISH -> PrometheusGetData")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

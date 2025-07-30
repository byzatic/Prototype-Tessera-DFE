#
#
#
from abc import ABCMeta, abstractmethod
from types import ModuleType
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from Global.NodeUnitDescription import NodeUnitDescription
from ServicePrometheus.i_WorkerContext import i_WorkerContext


class i_Worker(ModuleType):
    __metaclass__ = ABCMeta

    class WorkerMain(object):
        __metaclass__ = ABCMeta

        @abstractmethod
        def __init__(self,
                     abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                     configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                     application_context: i_WorkerContext,
                     current_node_description: NodeUnitDescription
                     ) -> None:
            self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
            self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
            self._application_context: i_WorkerContext = application_context
            self._current_node_description: NodeUnitDescription = current_node_description

        @abstractmethod
        def execute(self) -> None:
            pass

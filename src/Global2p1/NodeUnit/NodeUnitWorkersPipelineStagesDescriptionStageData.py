#
#
#
from .NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from .NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit

class NodeUnitWorkersPipelineStagesDescriptionStageData(object):
    def __init__(self, name: str, configuration: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit], abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit]):
        self.__name: str = name
        self.__configuration: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration
        self.__abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list

    def get_name(self) -> str:
        return self.__name

    def get_configuration(self) -> list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit]:
        return self.__configuration

    def get_abstract_data_list(self) -> list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit]:
        return self.__abstract_data_list

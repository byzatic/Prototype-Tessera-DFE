#
#
#
from .NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions
from typing import List, Optional, Union

class NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices(object):
    def __init__(self, id_name: str, description: str, options: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]):
        self.__id_name: str = id_name
        self.__description: str = description
        self.__options: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions] = options

    def get_id_name(self) -> str:
        return self.__id_name

    def get_description(self) -> str:
        return self.__description

    def get_options(self) -> list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions]:
        return self.__options

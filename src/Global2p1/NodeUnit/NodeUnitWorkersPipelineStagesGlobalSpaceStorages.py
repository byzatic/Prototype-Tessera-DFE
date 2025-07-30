#
#
#
from .NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions import NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions
from typing import List, Optional, Union


class NodeUnitWorkersPipelineStagesGlobalSpaceStorages(object):
    def __init__(self, id_name: str, description: str, options: list[NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions]):
        self.__id_name: str = id_name
        self.__description: str = description
        self.__options: list[NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions] = options

    def get_id_name(self) -> str:
        return self.__id_name

    def get_description(self) -> str:
        return self.__description

    def get_options(self) -> list[NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions]:
        return self.__options
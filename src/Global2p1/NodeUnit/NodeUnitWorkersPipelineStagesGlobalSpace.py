#
#
#
from .NodeUnitWorkersPipelineStagesGlobalSpaceStorages import NodeUnitWorkersPipelineStagesGlobalSpaceStorages
from .NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices import NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices
from typing import List, Optional, Union


class NodeUnitWorkersPipelineStagesGlobalSpace(object):
    def __init__(self, storages: list[NodeUnitWorkersPipelineStagesGlobalSpaceStorages], additional_services: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices]):
        self.__storages: list[NodeUnitWorkersPipelineStagesGlobalSpaceStorages] = storages
        self.__additional_services: list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices] = additional_services

    def get_storages(self) -> list[NodeUnitWorkersPipelineStagesGlobalSpaceStorages]:
        return self.__storages

    def get_additional_services(self) -> list[NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices]:
        return self.__additional_services

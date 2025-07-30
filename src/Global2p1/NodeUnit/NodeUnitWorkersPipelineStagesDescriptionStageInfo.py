#
#
#
from .NodeUnitWorkersPipelineStagesDescriptionStageData import NodeUnitWorkersPipelineStagesDescriptionStageData


class NodeUnitWorkersPipelineStagesDescriptionStageInfo(object):
    def __init__(self, stage_id: str, stage_data: list[NodeUnitWorkersPipelineStagesDescriptionStageData]):
        self.__stage_id: str = stage_id
        self.__stage_data: list[NodeUnitWorkersPipelineStagesDescriptionStageData] = stage_data

    def get_stage_id(self) -> str:
        return self.__stage_id

    def get_stage_data(self) -> list[NodeUnitWorkersPipelineStagesDescriptionStageData]:
        return self.__stage_data

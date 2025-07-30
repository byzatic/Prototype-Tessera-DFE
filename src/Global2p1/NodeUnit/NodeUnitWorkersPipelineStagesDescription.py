#
#
#
from .NodeUnitWorkersPipelineStagesDescriptionStageInfo import NodeUnitWorkersPipelineStagesDescriptionStageInfo


class NodeUnitWorkersPipelineStagesDescription(object):
    def __init__(self, stages_info: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo]):
        self.__stages_info: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo] = stages_info

    def get_stages_info(self) -> list[NodeUnitWorkersPipelineStagesDescriptionStageInfo]:
        return self.__stages_info

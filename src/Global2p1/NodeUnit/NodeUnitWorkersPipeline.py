#
#
#
from .NodeUnitWorkersPipelineStagesDescription import NodeUnitWorkersPipelineStagesDescription
from .NodeUnitWorkersPipelineStagesConsistency import NodeUnitWorkersPipelineStagesConsistency
from .NodeUnitWorkersPipelineStagesGlobalSpace import NodeUnitWorkersPipelineStagesGlobalSpace


class NodeUnitWorkersPipeline(object):
    def __init__(self, stages_consistency: list[NodeUnitWorkersPipelineStagesConsistency], stages_description: NodeUnitWorkersPipelineStagesDescription, global_space: NodeUnitWorkersPipelineStagesGlobalSpace):
        self.__global_space: NodeUnitWorkersPipelineStagesGlobalSpace = global_space
        self.__stages_consistency: list[NodeUnitWorkersPipelineStagesConsistency] = stages_consistency
        self.__stages_description: NodeUnitWorkersPipelineStagesDescription = stages_description

    def get_global_space(self) -> NodeUnitWorkersPipelineStagesGlobalSpace:
        return self.__global_space

    def get_stages_consistency(self) -> list[NodeUnitWorkersPipelineStagesConsistency]:
        return self.__stages_consistency

    def get_stages_description(self) -> NodeUnitWorkersPipelineStagesDescription:
        return self.__stages_description
#
#
#
from abc import ABCMeta, abstractmethod
from Global2p1.NodeUnit.NodeUnitWorkersPipeline import NodeUnitWorkersPipeline
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageData import NodeUnitWorkersPipelineStagesDescriptionStageData
from src.LibByzaticCommon.Singleton import Singleton


class i_PiplineManager(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def make_pipline(self, node_unit_workers_pipeline: NodeUnitWorkersPipeline) -> list[NodeUnitWorkersPipelineStagesDescriptionStageData]:
        pass
#
#
#
from abc import ABCMeta, abstractmethod
from LibByzaticCommon.Singleton import Singleton
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageData import NodeUnitWorkersPipelineStagesDescriptionStageData
from Global2p2.i_Worker import i_Worker
from Global.NodeUnitDescription import NodeUnitDescription


class i_WorkersRepository(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_worker(self, worker_stage_data: NodeUnitWorkersPipelineStagesDescriptionStageData, current_node_unit_description: NodeUnitDescription) -> i_Worker.WorkerMain:
        pass
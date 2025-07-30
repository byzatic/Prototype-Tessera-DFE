#
#
#
from abc import ABCMeta, abstractmethod
from Global2p2.i_Worker import i_Worker
from Global2p2.WorkerSpecification.WorkerSpecification import WorkerSpecification


class i_DaoWorkers():
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_worker(self, specification: WorkerSpecification) -> i_Worker:
        pass

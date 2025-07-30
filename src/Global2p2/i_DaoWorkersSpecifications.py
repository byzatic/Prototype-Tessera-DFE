#
#
#
from abc import ABCMeta, abstractmethod
from Global2p2.WorkerSpecification.WorkerSpecification import WorkerSpecification


class i_DaoWorkersSpecifications(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_worker_specification(self, worker_specification_name: str) -> WorkerSpecification:
        pass

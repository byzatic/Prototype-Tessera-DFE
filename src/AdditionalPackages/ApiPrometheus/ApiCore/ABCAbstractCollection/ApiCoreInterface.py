from abc import ABCMeta, abstractmethod
from multiprocessing import Queue


class ApiCoreInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, data_bridge_queue: Queue, host: str = "0.0.0.0", port: str = "8080"):
        pass

    @abstractmethod
    def run_core(self):
        pass

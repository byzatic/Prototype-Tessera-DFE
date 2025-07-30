from abc import ABCMeta, abstractmethod
from multiprocessing import Queue
from src.AdditionalPackages.ApiPrometheus.ApiPrometheusUnit import ApiPrometheusUnitInterface


class ApiPrometheusPublisherInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, data_bridge_queue: Queue):
        pass

    @abstractmethod
    def publish(self, api_prometheus_unit_list: list[ApiPrometheusUnitInterface]) -> None:
        pass

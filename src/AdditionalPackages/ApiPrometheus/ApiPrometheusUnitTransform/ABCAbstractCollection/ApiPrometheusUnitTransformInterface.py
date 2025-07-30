from abc import ABCMeta, abstractmethod
from src.AdditionalPackages.ApiPrometheus.ApiPrometheusUnit import ApiPrometheusUnitInterface


class ApiPrometheusUnitTransformInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def transform(self, api_prometheus_unit: ApiPrometheusUnitInterface) -> str:
        pass

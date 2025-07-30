from abc import ABCMeta, abstractmethod
from AdditionalPackages.DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration import PrometheusQueryConfiguration
from LibByzaticCommon.Singleton.Singleton import Singleton

class i_DaoPrometheusQueryConfigurations(Singleton):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def getPrometheusQueryConfigurationUnit(self, query_id: str) -> PrometheusQueryConfiguration:
        pass

    def getAllPrometheusQueryConfigurationUnits(self) -> list[PrometheusQueryConfiguration]:
        pass

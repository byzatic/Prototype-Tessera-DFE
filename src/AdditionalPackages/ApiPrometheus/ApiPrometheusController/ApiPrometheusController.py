from dataclasses import dataclass
from .ABCAbstractCollection import ApiPrometheusControllerInterface
from multiprocessing import Process
# идея в том что бы возвращать объект которым можно будет управлять api

@dataclass(frozen=True)
class ApiPrometheusUnit(ApiPrometheusControllerInterface):
    api_prometheus_process: Process = None
    metric_value: str = None

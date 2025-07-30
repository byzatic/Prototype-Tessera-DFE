from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from .i_DtoPrometheusMetricLabel import i_DtoPrometheusMetricLabel


@dataclass(frozen=True)
class i_DtoPrometheusMetric():
    __metaclass__ = ABCMeta

    def __init__(self,
                 value: str = None,
                 timestamp: str = None,
                 metric_labels: list[i_DtoPrometheusMetricLabel] = None
                 ) -> None:
        pass

    value: str = None
    timestamp: str = None
    metric_labels: list[i_DtoPrometheusMetricLabel] = None

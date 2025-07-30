from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from ..ApiPrometheusUnitLabel import ApiPrometheusUnitLabelInterface


@dataclass(frozen=True)
class ApiPrometheusUnitInterface():
    __metaclass__ = ABCMeta

    def __init__(self,
                 metric_name: str = None,
                 metric_value: str = None,
                 metric_labels: list[ApiPrometheusUnitLabelInterface] = None
                 ) -> None:
        pass

    metric_name: str = None
    metric_value: str = None
    metric_labels: list[ApiPrometheusUnitLabelInterface] = None

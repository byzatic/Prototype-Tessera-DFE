from dataclasses import dataclass
from .ABCAbstractCollection import PrometheusQueryLabelInterface


@dataclass(frozen=True)
class PrometheusQueryLabel(PrometheusQueryLabelInterface):
    label_value: str = None
    label_key: str = None
    label_sign: str = None


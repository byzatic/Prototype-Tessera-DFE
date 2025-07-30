#
#
#
from dataclasses import dataclass
from typing import Union
from .ABCAbstractCollection import PrometheusClientDtoInterface


@dataclass(frozen=True)
class PrometheusClientDto(PrometheusClientDtoInterface):
    data: Union[dict, list] = None
    status: str = None
    # Unix Timestamp
    ts: int = None

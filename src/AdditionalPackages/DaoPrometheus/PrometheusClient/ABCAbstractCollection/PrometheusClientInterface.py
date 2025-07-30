from abc import ABCMeta, abstractmethod
from ..PrometheusClientDto import PrometheusClientDtoInterface


class PrometheusClientInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_by_url(self, url: str, ssl_verify: bool) -> PrometheusClientDtoInterface:
        pass

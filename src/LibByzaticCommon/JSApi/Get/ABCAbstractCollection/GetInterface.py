from abc import ABCMeta, abstractmethod
from typing import Union


class PrometheusClientInterface(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get(self, url: str) -> Union[dict, list]:
        pass

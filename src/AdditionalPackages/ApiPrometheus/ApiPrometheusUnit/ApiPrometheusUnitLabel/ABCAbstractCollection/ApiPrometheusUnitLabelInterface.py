from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiPrometheusUnitLabelInterface(object):
    __metaclass__ = ABCMeta

    def __init__(self, label_value: str = None, label_key: str = None, label_sign: str = None) -> None:
        pass

    label_value: str = None
    label_key: str = None
    label_sign: str = None


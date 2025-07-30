from abc import ABCMeta, abstractmethod
from typing import Union


class i_DtoRawData(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def getData(self) -> Union[dict, list]:
        pass

    @abstractmethod
    def getStatus(self) -> str:
        pass

    @abstractmethod
    def getTs(self) -> int:
        pass






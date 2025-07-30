#
#
#
from typing import Union
from .i_DtoRawData import i_DtoRawData


class impl_DtoRawData(i_DtoRawData):
    
    __data: Union[dict, list] = None
    __status: str = None
    __ts: int = None

    def __init__(self,
                 data: Union[dict, list],
                 status: str,
                 ts: int
                 ) -> None:
        self.__data = data
        self.__status = status
        self.__ts = ts

    def getData(self) -> Union[dict, list]:
        return self.__data

    def getStatus(self) -> str:
        return self.__status

    def getTs(self) -> int:
        return self.__ts

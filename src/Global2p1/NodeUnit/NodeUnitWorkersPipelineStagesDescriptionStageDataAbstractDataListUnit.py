#
#
#
from typing import Optional


class NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit(object):
    def __init__(self, abstract_data_type: Optional[str] = None, abstract_data_specialty: Optional[str] = None, abstract_data_path: Optional[str] = None, abstract_data_key: Optional[str] = None, abstract_data_value: Optional[str] = None):
        self.__abstract_data_type: Optional[str] = abstract_data_type
        self.__abstract_data_specialty: Optional[str] = abstract_data_specialty
        self.__abstract_data_path: Optional[str] = abstract_data_path
        self.__abstract_data_key: Optional[str] = abstract_data_key
        self.__abstract_data_value: Optional[str] = abstract_data_value

    def get_abstract_data_type(self) -> Optional[str]:
        return self.__abstract_data_type

    def get_abstract_data_specialty(self) -> Optional[str]:
        return self.__abstract_data_specialty

    def get_abstract_data_path(self) -> Optional[str]:
        return self.__abstract_data_path

    def get_abstract_data_key(self) -> Optional[str]:
        return self.__abstract_data_key

    def get_abstract_data_value(self) -> Optional[str]:
        return self.__abstract_data_value

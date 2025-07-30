#
#
#


class NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit(object):
    def __init__(self, abstract_data_type: str, abstract_data_specialty: str, abstract_data_path: str, abstract_data_key: str, abstract_data_value: str):
        self.__abstract_data_type: str = abstract_data_type
        self.__abstract_data_specialty: str = abstract_data_specialty
        self.__abstract_data_path: str = abstract_data_path
        self.__abstract_data_key: str = abstract_data_key
        self.__abstract_data_value: str = abstract_data_value

    def get_abstract_data_type(self) -> str:
        return self.__abstract_data_type

    def get_abstract_data_specialty(self) -> str:
        return self.__abstract_data_specialty

    def get_abstract_data_path(self) -> str:
        return self.__abstract_data_path

    def get_abstract_data_key(self) -> str:
        return self.__abstract_data_key

    def get_abstract_data_value(self) -> str:
        return self.__abstract_data_value

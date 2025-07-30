#
#
#

class NodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions(object):
    def __init__(self, name: str, data: str):
        self.__name: str = name
        self.__data: str = data

    def get_name(self) -> str:
        return self.__name

    def get_data(self) -> str:
        return self.__data

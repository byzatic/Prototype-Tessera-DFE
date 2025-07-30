#
#
#


class NodeUnitWorkersPipelineStagesConsistency(object):
    def __init__(self, position: str, name: str):
        self.__position: str = position
        self.__name: str = name

    def get_position(self) -> str:
        return self.__position

    def get_name(self) -> str:
        return self.__name

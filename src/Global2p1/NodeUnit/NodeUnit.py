#
#
#
from .NodeUnitOption import NodeUnitOption
from .NodeUnitWorkersPipeline import NodeUnitWorkersPipeline


class NodeUnit(object):
    def __init__(self, options: list[NodeUnitOption], workers_pipeline: NodeUnitWorkersPipeline, downstream: list[str], upstream: list[str], node_id: str):
        self.__options: list[NodeUnitOption] = options
        self.__workers_pipeline: NodeUnitWorkersPipeline = workers_pipeline
        self.__downstream: list[str] = downstream
        self.__upstream: list[str] = upstream
        self.__node_id: str = node_id

    def get_options(self) -> list[NodeUnitOption]:
        return self.__options

    def get_workers_pipeline(self) -> NodeUnitWorkersPipeline:
        return self.__workers_pipeline

    def get_downstream(self) -> list[str]:
        return self.__downstream

    def get_upstream(self) -> list[str]:
        return self.__upstream

    def get_node_id(self) -> str:
        return self.__node_id

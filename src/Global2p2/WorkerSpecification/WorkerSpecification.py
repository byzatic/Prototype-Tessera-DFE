#
#
#
from .WorkerSpecificationDefaultOption import WorkerSpecificationDefaultOption


class WorkerSpecification(object):
    def __init__(self, name: str, module_main_path: str, default_options: list[WorkerSpecificationDefaultOption]):
        self.__name: str = name
        self.__module_main_path: str = module_main_path
        self.__default_options: list[WorkerSpecificationDefaultOption] = default_options

    def get_name(self) -> str:
        return self.__name

    def get_module_main_path(self) -> str:
        return self.__module_main_path

    def get_default_options(self) -> list[WorkerSpecificationDefaultOption]:
        return self.__default_options

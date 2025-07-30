#
#
#


class WorkerSpecificationDefaultOption(object):
    def __init__(self, default_option_name: str, default_option_value: str):
        self.__default_option_name: str = default_option_name
        self.__default_option_value: str = default_option_value

    def get_default_option_name(self) -> str:
        return self.__default_option_name

    def get_default_option_value(self) -> str:
        return self.__default_option_value

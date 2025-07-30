#
#
#


class NodeUnitOption(object):
    def __init__(self, option_name: str, option_value: str):
        self.__option_name: str = option_name
        self.__option_value: str = option_value

    def get_option_name(self) -> str:
        return self.__option_name

    def get_option_value(self) -> str:
        return self.__option_value

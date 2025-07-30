#
#
#


class DtoLabel(object):
    def __init__(self, label_name: str, label_value: str, label_sign: str):
        self.__label_name: str = label_name
        self.__label_value: str = label_value
        self.__label_sign: str = label_sign

    def getLabelName(self) -> str:
        return self.__label_name

    def getLabelSign(self) -> str:
        return self.__label_sign

    def getLabelValue(self) -> str:
        return self.__label_value




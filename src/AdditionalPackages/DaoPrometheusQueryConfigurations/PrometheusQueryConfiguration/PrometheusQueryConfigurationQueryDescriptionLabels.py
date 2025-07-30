#
#
#


class PrometheusQueryConfigurationQueryDescriptionLabels(object):
    def __init__(self, label_key: str, label_sign: str, label_value: str):
        self.__label_key: str = label_key
        self.__label_sign: str = label_sign
        self.__label_value: str = label_value

    def getLabelKey(self) -> str:
        return self.__label_key

    def getLabelSign(self) -> str:
        return self.__label_sign

    def getLabelValue(self) -> str:
        return self.__label_value

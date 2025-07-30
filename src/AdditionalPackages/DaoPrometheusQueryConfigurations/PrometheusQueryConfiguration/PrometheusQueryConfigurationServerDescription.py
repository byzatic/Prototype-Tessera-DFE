#
#
#


class PrometheusQueryConfigurationServerDescription(object):
    def __init__(self, url: str, ssl_verify: str):
        self.__url: str = url
        self.__ssl_verify: str = ssl_verify

    def getUrl(self) -> str:
        return self.__url

    def getSslVerify(self) -> str:
        return self.__ssl_verify

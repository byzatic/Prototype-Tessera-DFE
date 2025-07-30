#
#
#


class DtoNodeUnitStorage(object):
    def __init__(self, local_storage: dict):
        self.__storage: dict = local_storage

    def get_storage(self):
        return self.__storage

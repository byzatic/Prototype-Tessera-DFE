#
#
from LibByzaticCommon.Exceptions.BaseErrorException import BaseErrorException
from errno import ENOTRECOVERABLE


class ServerUnavailableException(BaseErrorException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        if kwargs.get('errno') is not None:
            self.errno: int = kwargs.get('errno')
        else:
            # ENOTRECOVERABLE - State not recoverable
            self.errno: int = ENOTRECOVERABLE

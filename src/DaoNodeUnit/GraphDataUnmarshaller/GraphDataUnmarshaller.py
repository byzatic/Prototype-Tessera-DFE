#
#
#
import logging
from marshmallow import RAISE
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnit
from DaoNodeUnit.MrshmellowModels.ModelDtoRawGraphData import SchemaDtoRawGraphDataNodeUnit
from DaoNodeUnit.LocalApi.InterfaceGraphDataUnmarshaller import InterfaceGraphDataUnmarshaller
from LibByzaticCommon import Exceptions


class GraphDataUnmarshaller(InterfaceGraphDataUnmarshaller):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("DaoNodeUnit-logger")
        self.__DtoSerializationSchema: SchemaDtoRawGraphDataNodeUnit = SchemaDtoRawGraphDataNodeUnit()

    def unmarshal(self, raw_data: dict) -> DtoRawGraphDataNodeUnit:
        try:
            if raw_data is None or raw_data == {}:
                raise Exceptions.OperationIncompleteException("Graph data is empty, nothing to unmarshal")
            else:
                return self.__DtoSerializationSchema.load(data=raw_data, unknown=RAISE)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as err:
            raise Exceptions.OperationIncompleteException(err.args)

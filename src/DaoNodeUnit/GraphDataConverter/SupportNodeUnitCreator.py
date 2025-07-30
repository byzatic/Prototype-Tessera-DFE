#
#
#
import logging

# DtoRawGraphData
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnit
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitOption
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipeline

# DtoRawGraphData
from Global2p1.NodeUnit import NodeUnit
from Global2p1.NodeUnit import NodeUnitOption
from Global2p1.NodeUnit import NodeUnitWorkersPipeline

from DaoNodeUnit.MrshmellowModels.ModelDtoRawGraphData import SchemaDtoRawGraphDataNodeUnit
from DaoNodeUnit.MrshmellowModels.ModelDtoRawGraphData import SchemaDtoRawGraphDataNodeUnitOption
from DaoNodeUnit.MrshmellowModels.ModelDtoRawGraphData import SchemaDtoRawGraphDataNodeUnitWorkersPipeline
# TODO: --> SchemaDtoNodeUnit should be renamed to SchemaNodeUnit
from DaoNodeUnit.MrshmellowModels.ModelDtoNodeUnit import SchemaDtoNodeUnit
from DaoNodeUnit.MrshmellowModels.ModelDtoNodeUnit import SchemaDtoNodeUnitOption
from DaoNodeUnit.MrshmellowModels.ModelDtoNodeUnit import SchemaDtoNodeUnitWorkersPipeline

from src.LibByzaticCommon import Exceptions


class SupportNodeUnitCreator(object):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("DaoNodeUnit-logger")
        self.__SchemaDtoRawGraphDataNodeUnit = SchemaDtoRawGraphDataNodeUnit()
        self.__SchemaDtoRawGraphDataNodeUnitOption = SchemaDtoRawGraphDataNodeUnitOption()
        self.__SchemaDtoRawGraphDataNodeUnitWorkersPipeline = SchemaDtoRawGraphDataNodeUnitWorkersPipeline()
        self.__SchemaDtoNodeUnit = SchemaDtoNodeUnit()
        self.__SchemaDtoNodeUnitOption = SchemaDtoNodeUnitOption()
        self.__SchemaDtoNodeUnitWorkersPipeline = SchemaDtoNodeUnitWorkersPipeline()

    def create_node_unit_from_node_raw(self, dto_raw_graph_data_node_unit: DtoRawGraphDataNodeUnit, downstream: list[str], upstream: list[str], node_id: str) -> NodeUnit:
        try:
            new_options: list[NodeUnitOption] = self.__get_options_list(dto_raw_graph_data_node_unit.options)
            new_workers_pipeline: NodeUnitWorkersPipeline = self.__get_workers_pipeline(dto_raw_graph_data_node_unit.workers_pipeline)
            new_node_unit: NodeUnit = NodeUnit(
                options=new_options,
                workers_pipeline=new_workers_pipeline,
                downstream=downstream,
                upstream=upstream,
                node_id=node_id
            )
            return new_node_unit
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __get_options_list(self, raw_options: list[DtoRawGraphDataNodeUnitOption]) -> list[NodeUnitOption]:
        self.__logger.debug(f"SupportNodeUnitCreator -> __get_options_list -> start << {raw_options}")
        new_options: list[NodeUnitOption] = []
        for raw_options_unit in raw_options:
            new_option: NodeUnitOption = NodeUnitOption(
                option_name=raw_options_unit.option_name,
                option_value=raw_options_unit.option_value
            )
            new_options.append(new_option)
        self.__logger.debug(f"SupportNodeUnitCreator -> __get_options_list -> finish >> {raw_options}")
        return new_options

    def __get_workers_pipeline(self, raw_workers_pipeline: DtoRawGraphDataNodeUnitWorkersPipeline) -> NodeUnitWorkersPipeline:
        try:
            self.__logger.debug(f"SupportNodeUnitCreator -> __get_workers_pipeline -> start << {raw_workers_pipeline}")
            marshalled_workers_pipeline = self.__SchemaDtoRawGraphDataNodeUnitWorkersPipeline.dump(raw_workers_pipeline)
            self.__logger.debug(f"SupportNodeUnitCreator -> __get_workers_pipeline -> marshalled_workers_pipeline: {marshalled_workers_pipeline}")
            node_unit_workers_pipeline: NodeUnitWorkersPipeline = self.__SchemaDtoNodeUnitWorkersPipeline.load(marshalled_workers_pipeline)
            self.__logger.debug(f"SupportNodeUnitCreator -> __get_workers_pipeline -> finish >> {node_unit_workers_pipeline}")
            return node_unit_workers_pipeline
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)
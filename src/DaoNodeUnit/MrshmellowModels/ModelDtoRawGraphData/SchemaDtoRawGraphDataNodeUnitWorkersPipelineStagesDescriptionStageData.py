#
#
#
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from marshmallow import Schema, fields, post_load
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData(Schema):
    name = fields.String(required=True)
    configuration = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit, required=True))
    abstract_data_list = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData(**data)

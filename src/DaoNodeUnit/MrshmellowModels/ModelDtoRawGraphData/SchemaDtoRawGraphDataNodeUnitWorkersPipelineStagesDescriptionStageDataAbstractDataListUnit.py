#
#
#
from marshmallow import Schema, fields, post_load
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit(Schema):
    abstract_data_type = fields.String(required=True, allow_none=True)
    abstract_data_specialty = fields.String(required=True, allow_none=True)
    abstract_data_path = fields.String(required=True, allow_none=True)
    abstract_data_key = fields.String(required=True, allow_none=True)
    abstract_data_value = fields.String(required=True, allow_none=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit(**data)

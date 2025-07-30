#
#
#
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData
from marshmallow import Schema, fields, post_load
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo(Schema):
    stage_id = fields.String(required=True)
    stage_data = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageData, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo(**data)

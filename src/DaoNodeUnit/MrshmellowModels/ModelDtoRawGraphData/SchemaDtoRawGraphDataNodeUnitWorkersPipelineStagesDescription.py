#
#
#
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo
from src.DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesDescription
from marshmallow import Schema, fields, post_load


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescription(Schema):
    stages_info = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesDescriptionStageInfo, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesDescription(**data)

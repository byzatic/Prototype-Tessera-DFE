#
#
#
from .SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageInfo import SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageInfo
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesDescription
from marshmallow import Schema, fields, post_load


class SchemaDtoNodeUnitWorkersPipelineStagesDescription(Schema):
    stages_info = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageInfo, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesDescription(**data)

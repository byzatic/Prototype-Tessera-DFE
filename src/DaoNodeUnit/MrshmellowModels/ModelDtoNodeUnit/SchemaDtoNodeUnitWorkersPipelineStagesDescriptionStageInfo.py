#
#
#
from .SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageData import SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageData
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesDescriptionStageInfo


class SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageInfo(Schema):
    stage_id = fields.String(required=True)
    stage_data = fields.List(fields.Nested(SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageData, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesDescriptionStageInfo(**data)

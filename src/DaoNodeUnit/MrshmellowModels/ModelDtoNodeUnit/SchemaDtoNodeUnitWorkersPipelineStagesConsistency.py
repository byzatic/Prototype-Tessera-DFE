#
#
#
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesConsistency


class SchemaDtoNodeUnitWorkersPipelineStagesConsistency(Schema):
    position = fields.Integer(required=True)
    name = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesConsistency(**data)

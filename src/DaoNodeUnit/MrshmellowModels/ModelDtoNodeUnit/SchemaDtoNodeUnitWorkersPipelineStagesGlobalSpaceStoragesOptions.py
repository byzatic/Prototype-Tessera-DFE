#
#
#
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions


class SchemaDtoNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions(Schema):
    name = fields.String(required=True)
    data = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions(**data)

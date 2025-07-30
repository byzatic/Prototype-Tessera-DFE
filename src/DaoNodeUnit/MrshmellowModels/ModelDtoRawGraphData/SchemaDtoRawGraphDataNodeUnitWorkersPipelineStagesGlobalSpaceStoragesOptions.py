#
#
#
from marshmallow import Schema, fields, post_load
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions(Schema):
    name = fields.String(required=True)
    data = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions(**data)

#
#
#
from marshmallow import Schema, fields, post_load
from DaoNodeUnit.DtoRawGraphData import DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices
from .SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions import SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions


class SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices(Schema):
    id_name = fields.String(required=True)
    description = fields.String(required=True)
    options = fields.List(fields.Nested(SchemaDtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServicesOptions, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return DtoRawGraphDataNodeUnitWorkersPipelineStagesGlobalSpaceAdditionalServices(**data)

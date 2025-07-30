#
#
#
from marshmallow import Schema, fields, post_load
from Global2p1.NodeUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit


class SchemaDtoNodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit(Schema):
    abstract_data_type = fields.String(required=True)
    abstract_data_specialty = fields.String(required=True)
    abstract_data_path = fields.String(required=True)
    abstract_data_key = fields.String(required=True)
    abstract_data_value = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit(**data)

#
#
from marshmallow import Schema, fields, post_load
from Global2p2.WorkerSpecification.WorkerSpecificationDefaultOption import WorkerSpecificationDefaultOption


class SchemaWorkerSpecificationDefaultOption(Schema):
    default_option_name = fields.String(required=True)
    default_option_value = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return WorkerSpecificationDefaultOption(**data)

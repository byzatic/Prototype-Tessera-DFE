#
#
#
from marshmallow import Schema, fields, post_load
from Global2p2.WorkerSpecification.WorkerSpecification import WorkerSpecification
from .SchemaWorkerSpecificationDefaultOption import SchemaWorkerSpecificationDefaultOption


class SchemaWorkerSpecification(Schema):
    name = fields.String(required=True)
    module_main_path = fields.String(required=True)
    default_options = fields.List(fields.Nested(SchemaWorkerSpecificationDefaultOption, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return WorkerSpecification(**data)

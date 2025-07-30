#
#
from marshmallow import Schema, fields, post_load
from .SchemaPrometheusQueryConfigurationServerDescription import SchemaPrometheusQueryConfigurationServerDescription
from .SchemaPrometheusQueryConfigurationQueryDescription import SchemaPrometheusQueryConfigurationQueryDescription
from AdditionalPackages.DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration.PrometheusQueryConfiguration import PrometheusQueryConfiguration


class SchemaPrometheusQueryConfiguration(Schema):
    server_description = fields.Nested(SchemaPrometheusQueryConfigurationServerDescription, many=False, required=True)
    query_description = fields.List(fields.Nested(SchemaPrometheusQueryConfigurationQueryDescription, many=False, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return PrometheusQueryConfiguration(**data)


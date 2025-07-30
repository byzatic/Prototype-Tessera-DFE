#
#
#
from marshmallow import Schema, fields, post_load
from AdditionalPackages.DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration.PrometheusQueryConfigurationServerDescription import PrometheusQueryConfigurationServerDescription


class SchemaPrometheusQueryConfigurationServerDescription(Schema):
    url = fields.String(required=True)
    ssl_verify = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return PrometheusQueryConfigurationServerDescription(**data)

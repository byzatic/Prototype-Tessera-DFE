#
#
#
from marshmallow import Schema, fields, post_load
from .SchemaPrometheusQueryConfigurationQueryDescriptionLabels import SchemaPrometheusQueryConfigurationQueryDescriptionLabels
from AdditionalPackages.DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration.PrometheusQueryConfigurationQueryDescription import PrometheusQueryConfigurationQueryDescription


class SchemaPrometheusQueryConfigurationQueryDescription(Schema):
    query_id = fields.String(required=True)
    query_type = fields.String(required=True)
    upper_limit = fields.String(required=True)
    lower_limit = fields.String(required=True)
    step = fields.String(required=True)
    time_range = fields.String(required=True)
    labels = fields.List(fields.Nested(SchemaPrometheusQueryConfigurationQueryDescriptionLabels, many=False, required=True))

    @post_load
    def make_dto(self, data, **kwargs):
        return PrometheusQueryConfigurationQueryDescription(**data)

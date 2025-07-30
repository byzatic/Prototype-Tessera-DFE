#
#
#
from marshmallow import Schema, fields, post_load
from AdditionalPackages.DaoPrometheusQueryConfigurations.PrometheusQueryConfiguration.PrometheusQueryConfigurationQueryDescriptionLabels import PrometheusQueryConfigurationQueryDescriptionLabels


class SchemaPrometheusQueryConfigurationQueryDescriptionLabels(Schema):
    label_key = fields.String(required=True)
    label_sign = fields.String(required=True)
    label_value = fields.String(required=True)

    @post_load
    def make_dto(self, data, **kwargs):
        return PrometheusQueryConfigurationQueryDescriptionLabels(**data)

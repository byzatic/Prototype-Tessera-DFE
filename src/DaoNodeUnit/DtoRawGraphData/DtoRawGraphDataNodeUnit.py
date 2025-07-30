#
# nested – Schema instance, class, class name (string), dictionary, or callable that returns a Schema or dictionary. Dictionaries are converted with Schema.from_dict.
# only – A list or tuple of fields to marshal. If None, all fields are marshalled. This parameter takes precedence over exclude.
# exclude – A list or tuple of fields to exclude.
# many – Whether the field is a collection of objects.
# unknown – Whether to exclude, include, or raise an error for unknown fields in the data. Use EXCLUDE, INCLUDE or RAISE.
# kwargs – The same keyword arguments that Field receives.
#
from .DtoRawGraphDataNodeUnitOption import DtoRawGraphDataNodeUnitOption
from .DtoRawGraphDataNodeUnitWorkersPipeline import DtoRawGraphDataNodeUnitWorkersPipeline
from marshmallow import Schema, fields, validate, post_load
from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class DtoRawGraphDataNodeUnit:
    options: List[DtoRawGraphDataNodeUnitOption]
    workers_pipeline: DtoRawGraphDataNodeUnitWorkersPipeline
    downstream: List


#
#
#
import logging
from .DtoLabel import DtoLabel
from typing import Optional
from LibByzaticCommon import Exceptions


class LabelParser(object):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("LabelParser-logger")

    def struct(self, label_str: str) -> DtoLabel:
        try:

            if label_str is None:
                raise Exceptions.OperationIncompleteException(f"Incorrect label string {label_str}")

            new_label_str: Optional[str] = None

            if label_str[0] == "{" and label_str[-1] == "}":
                list_char_0 = label_str
                list_char_1 = list_char_0[:-1]
                list_char_2 = list_char_1[1:]
                new_label_str = list_char_2
            else:
                raise Exceptions.OperationIncompleteException(f"Incorrect label string: {label_str}")

            if new_label_str is None:
                raise Exceptions.OperationIncompleteException(f"Incorrect new label string: {new_label_str}")

            label_str_delimiter: str = self.__get_delimiter(new_label_str)

            new_dto: DtoLabel = DtoLabel(
                label_name=new_label_str.split(label_str_delimiter, 1)[0],
                label_value=new_label_str.split(label_str_delimiter, 1)[1],
                label_sign=label_str_delimiter
            )
            return new_dto
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def destruct(self, dto_label: DtoLabel) -> str:
        try:
            final_str: str = "{" + dto_label.getLabelName() + dto_label.getLabelSign() + dto_label.getLabelValue() + "}"
            return final_str
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __get_delimiter(self, label_str: str) -> str:
        sign_count_1 = label_str.count("=")
        if sign_count_1 >= 1:
            return "="
        else:
            raise Exceptions.OperationIncompleteException(f"Can't found delimiter in label string {label_str}")

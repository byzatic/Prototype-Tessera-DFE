#
#
#
import logging
from typing import Optional
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit import NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit
from Global2p2.i_StorageManager import i_StorageManager
from Global.NodeUnitDescription import NodeUnitDescription
from ServicePrometheus.i_WorkerContext import i_WorkerContext
from Global2p2.i_Storage import i_Storage
from Global2p2.i_StorageItem import i_StorageItem
from modules.graphite_application_modules.Global.StorageItem import StorageItem
from modules.graphite_application_modules.Global.StorageItemValue import StorageItemValue
from LibByzaticCommon import Exceptions
from .SupportCreatorStorageItem import SupportCreatorStorageItem
from modules.graphite_application_modules.Global.LabelParser.DtoLabel import DtoLabel
from modules.graphite_application_modules.Global.LabelParser.LabelParser import LabelParser


class ModuleProcess(object):
    def __init__(self, abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit],
                 configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit],
                 application_context: i_WorkerContext,
                 current_node_description: NodeUnitDescription
                 ):
        self.__logger: logging.Logger = logging.getLogger("Workers-ProcessingStatus-logger")
        self._abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = abstract_data_list
        self._configuration_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataConfigurationUnit] = configuration_list
        self._application_context: i_WorkerContext = application_context
        self._current_node_description: NodeUnitDescription = current_node_description
        self._storage_manager: i_StorageManager = self._application_context.getStorageManager()
        self.__SupportCreatorStorageItem: SupportCreatorStorageItem = SupportCreatorStorageItem()
        self.__LabelParser: LabelParser = LabelParser()

    def run(self):
        output_storage: i_Storage = self.__get_output_storage()
        input_storage: i_Storage = self.__get_input_storage()

        input_abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = self.__get_input_abstract_data_list()
        output_data_item: NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit = self.__get_output_data_item()
        local_reason_tag: str = self.__search_local_reason_tag(output_data_item.get_abstract_data_specialty())

        max_value: int = 0
        reason_tag: Optional[str] = None

        for input_abstract_data in input_abstract_data_list:
            local_data_item: i_StorageItem = input_storage.read(input_abstract_data.get_abstract_data_specialty())
            if isinstance(local_data_item, StorageItem):
                local_data_item_value: StorageItemValue = local_data_item.getValue()
                local_data_item_value_value: str = local_data_item_value.getValue()
                if local_data_item_value_value.isdigit():
                    local_data_item_value_value_digit: int = int(local_data_item_value_value)
                else:
                    raise Exceptions.OperationIncompleteException(f"Incorrect type of value")
                local_data_item_reason_tag: Optional[str] = self.__search_data_item_reason_tag(local_data_item_value.getLabel())

                if local_data_item_value_value_digit > max_value:
                    self.__logger.debug(f"data item value ({local_data_item_value_value_digit}) > max value ({max_value})")
                    max_value = local_data_item_value_value_digit
                    reason_tag = self.__upgrade_reason_tag(reason_tag, local_reason_tag, local_data_item_reason_tag)
                elif local_data_item_value_value_digit == max_value and max_value > 0:
                    self.__logger.debug(f"data item value ({local_data_item_value_value_digit}) = max value ({max_value}) and > 0")
                    reason_tag = self.__upgrade_reason_tag(reason_tag, local_reason_tag, local_data_item_reason_tag)
            else:
                raise Exceptions.OperationIncompleteException(f"Incorrect type of storage item")

        label_list: list[str] = []
        if reason_tag is not None:
            label_list.append(reason_tag)
        label_list.append(self.__get_output_node_label())

        self.__logger.debug(f"Creating storage item with >> name = {self.__get_output_data_key()}")
        self.__logger.debug(f"Creating storage item with >> value = {str(max_value)}")
        self.__logger.debug(f"Creating storage item with >> labels = {label_list}")
        storage_item: i_StorageItem = self.__SupportCreatorStorageItem.create_StorageItem(
            name=self.__get_output_data_key(),
            value=str(max_value),
            labels=label_list
        )
        output_storage.create(self.__get_output_data_name(), storage_item)
        self._storage_manager.put_storage(self.__get_output_storage_name(), output_storage, self._current_node_description)

    def __upgrade_reason_tag(self, current_reason_tag: Optional[str], local_reason_tag: str, extension_reason_tag: Optional[str]) -> str:
        """
        current_reason_tag - reason tag in process (might be None)
        local_reason_tag - reason tag of executor
        extension_reason_tag - reason tag of data (might be None)

        returns updated current_reason_tag
        """

        parsed_local_reason_tag = self.__LabelParser.struct(local_reason_tag)

        if current_reason_tag is not None:
            parsed_current_reason_tag = self.__LabelParser.struct(current_reason_tag)
            if extension_reason_tag is not None:
                parsed_extension_reason_tag = self.__LabelParser.struct(extension_reason_tag)
                upgraded_reason_tag: str = ("{"
                                            + parsed_current_reason_tag.getLabelName()
                                            + parsed_current_reason_tag.getLabelSign()
                                            + parsed_current_reason_tag.getLabelValue() + "; "
                                            + parsed_extension_reason_tag.getLabelValue() + "; "
                                            + "}")
            else:
                upgraded_reason_tag: str = ("{"
                                            + parsed_current_reason_tag.getLabelName()
                                            + parsed_current_reason_tag.getLabelSign()
                                            + parsed_current_reason_tag.getLabelValue() + "; "
                                            + "}")
        else:
            default_reason_tag: str = "{reason=NONE}"
            parsed_current_reason_tag = self.__LabelParser.struct(default_reason_tag)
            if extension_reason_tag is not None:
                parsed_extension_reason_tag = self.__LabelParser.struct(extension_reason_tag)
                upgraded_reason_tag: str = ("{"
                                            + parsed_current_reason_tag.getLabelName()
                                            + parsed_current_reason_tag.getLabelSign()
                                            + parsed_local_reason_tag.getLabelValue() + "; "
                                            + parsed_extension_reason_tag.getLabelValue() + "; "
                                            + "}")
            else:
                upgraded_reason_tag: str = ("{"
                                            + parsed_current_reason_tag.getLabelName()
                                            + parsed_current_reason_tag.getLabelSign()
                                            + parsed_local_reason_tag.getLabelValue() + "; "
                                            + "}")
        return upgraded_reason_tag

    def __get_input_abstract_data_list(self) -> list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit]:
        input_abstract_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = []
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "InputData":
                input_abstract_data_list.append(abstract_data)
        self.__logger.debug(f"found {len(input_abstract_data_list)} InputData items")
        return input_abstract_data_list

    def __search_local_reason_tag(self, search_specialty) -> str:
        local_reason_tag: Optional[str] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputDataLabel":
                self.__logger.debug( f"Found OutputDataLabel")
                if abstract_data.get_abstract_data_specialty() == search_specialty:
                    self.__logger.debug(f"abstract data specialty {abstract_data.get_abstract_data_specialty()} equals search specialty {search_specialty}")
                    if abstract_data.get_abstract_data_key() == "label-specific-reason":
                        local_reason_tag = abstract_data.get_abstract_data_value()
                        self.__logger.debug(f"abstract data value {abstract_data.get_abstract_data_key()} equals label-specific-reason")
                        break
                    else:
                        self.__logger.debug(f"Not found label-specific-reason in OutputDataLabel")
                else:
                    self.__logger.debug(f"Found abstract data with abstract data specialty {abstract_data.get_abstract_data_specialty()}, not {search_specialty}")
            else:
                self.__logger.debug(f"Found abstract data with data type {abstract_data.get_abstract_data_type()}, not OutputDataLabel")

        if local_reason_tag is not None:
            self.__logger.debug(f"found local reason tag")
            return local_reason_tag
        else:
            raise Exceptions.OperationIncompleteException(f"Input storage with label-specific-reason not found")

    def __get_output_data_item(self) -> NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit:
        output_data_item: Optional[NodeUnitWorkersPipelineStagesDescriptionStageDataAbstractDataListUnit] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputData":
                output_data_item = abstract_data
                break
        if output_data_item is not None:
            return output_data_item
        else:
            raise Exceptions.OperationIncompleteException(f"OutputData not found")

    def __search_data_item_reason_tag(self, list_str_tags: list[str]) -> Optional[str]:
        data_item_reason_tag: Optional[str] = None
        for str_tag in list_str_tags:
            marshalled_str_tag = self.__LabelParser.struct(str_tag)
            if marshalled_str_tag.getLabelName() == "reason":
                data_item_reason_tag = str_tag
                break
        if data_item_reason_tag is not None:
            self.__logger.debug(f"reason tag found")
            return data_item_reason_tag
        else:
            self.__logger.debug(f"reason tag not found")
            return data_item_reason_tag

    def __get_final_storage_item(self) -> i_StorageItem:

        input_storage: i_Storage = self.__get_input_storage()

        max_value: int = 0
        label_list: list[str] = []
        reason_tag: Optional[str] = None

        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "InputData":
                self.__logger.debug(f"input data id is {abstract_data.get_abstract_data_specialty()}")

                input_storage_item: i_StorageItem = input_storage.read(abstract_data.get_abstract_data_specialty())

                if isinstance(input_storage_item, StorageItem):
                    raw_data_value_object: StorageItemValue = input_storage_item.getValue()

                    raw_data_value: str = input_storage_item.getValue().getValue()
                    if raw_data_value is None:
                        raise Exceptions.OperationIncompleteException(f"Unexpected value <{raw_data_value}>")
                    if raw_data_value.isdigit():
                        int_raw_data_value: int = int(raw_data_value)
                    else:
                        raise Exceptions.OperationIncompleteException(f"Incorrect type of data in StorageItem << StorageItemValue << value, must be digit")

                    self.__logger.debug(f"Found null status {str(int_raw_data_value)}")

                    if max_value < int_raw_data_value:
                        max_value = int_raw_data_value
                        self.__logger.debug(f"status saved")

                        local_reason_tag: Optional[str] = self.__search_for_reason_tag(raw_data_value_object.getLabel())
                        lcoal_reason_extension: str = self.__get_reason_extension()

                        if reason_tag is not None:
                            if local_reason_tag is not None:
                                structed_reason_tag: DtoLabel = self.__LabelParser.struct(reason_tag)
                                new_reason_tag_value = f"{structed_reason_tag.getLabelValue()}; {self.__LabelParser.struct(local_reason_tag).getLabelValue()}"
                                structed_reason_tag: DtoLabel = DtoLabel(
                                    label_name=structed_reason_tag.getLabelName(),
                                    label_value=new_reason_tag_value,
                                    label_sign=structed_reason_tag.getLabelSign()
                                )
                                reason_tag = self.__LabelParser.destruct(structed_reason_tag)
                            else:
                                reason_tag = reason_tag
                        else:
                            if local_reason_tag is not None:
                                new_reason_tag_value = f"{self.__LabelParser.struct(lcoal_reason_extension).getLabelValue()}; {self.__LabelParser.struct(local_reason_tag).getLabelValue()}"
                                structed_reason_tag: DtoLabel = DtoLabel(
                                    label_name=self.__LabelParser.struct(local_reason_tag).getLabelName(),
                                    label_value=new_reason_tag_value,
                                    label_sign=self.__LabelParser.struct(local_reason_tag).getLabelSign()
                                )
                                reason_tag = self.__LabelParser.destruct(structed_reason_tag)
                            else:
                                reason_tag = lcoal_reason_extension
                        self.__logger.debug(f"reason tag saved")

                    elif max_value == int_raw_data_value:

                        local_reason_tag: Optional[str] = self.__search_for_reason_tag(raw_data_value_object.getLabel())
                        lcoal_reason_extension: str = self.__get_reason_extension()

                        if reason_tag is not None:
                            if local_reason_tag is not None:
                                structed_reason_tag: DtoLabel = self.__LabelParser.struct(reason_tag)
                                new_reason_tag_value = f"{structed_reason_tag.getLabelValue()}; {self.__LabelParser.struct(local_reason_tag).getLabelValue()}"
                                structed_reason_tag: DtoLabel = DtoLabel(
                                    label_name=structed_reason_tag.getLabelName(),
                                    label_value=new_reason_tag_value,
                                    label_sign=structed_reason_tag.getLabelSign()
                                )
                                reason_tag = self.__LabelParser.destruct(structed_reason_tag)
                            else:
                                reason_tag = reason_tag
                        else:
                            if local_reason_tag is not None:
                                new_reason_tag_value = f"{self.__LabelParser.struct(lcoal_reason_extension).getLabelValue()}; {self.__LabelParser.struct(local_reason_tag).getLabelValue()}"
                                structed_reason_tag: DtoLabel = DtoLabel(
                                    label_name=self.__LabelParser.struct(local_reason_tag).getLabelName(),
                                    label_value=new_reason_tag_value,
                                    label_sign=self.__LabelParser.struct(local_reason_tag).getLabelSign()
                                )
                                reason_tag = self.__LabelParser.destruct(structed_reason_tag)
                            else:
                                reason_tag = lcoal_reason_extension
                        self.__logger.debug(f"reason tag saved")

                    elif max_value > int_raw_data_value:
                        pass
                    else:
                        raise Exceptions.OperationIncompleteException(f"I don't know what is going on there...")

        label_list.append(self.__get_output_node_label())
        self.__logger.debug(f"`node label` added to labels list")
        self.__logger.debug(f"reason tag finalised: {reason_tag}")
        if reason_tag is not None:
            label_list.append(reason_tag)
        storage_item: i_StorageItem = self.__SupportCreatorStorageItem.create_StorageItem(
            name=self.__get_output_data_key(),
            value=str(max_value),
            labels=label_list
        )
        return storage_item

    def __search_for_reason_tag(self, tag_list: list[str]) -> Optional[str]:
        reason_tag: Optional[str] = None
        for tag in tag_list:
            structed_label: DtoLabel = self.__LabelParser.struct(tag)
            if structed_label.getLabelName() == "reason":
                reason_tag = self.__LabelParser.destruct(structed_label)
                break
        if reason_tag is not None:
            self.__logger.debug("found reason tag")
            return reason_tag
        else:
            self.__logger.warning(f"reason tag not found")
            return None

    def __get_reason_extension(self) -> str:
        self.__logger.debug(f"Search for reason extension")
        reason_extension: Optional[str] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputDataLabel" and abstract_data.get_abstract_data_key() == "label-specific-reason":
                reason_extension = abstract_data.get_abstract_data_value()
                break
        if reason_extension is not None:
            return reason_extension
        else:
            raise Exceptions.OperationIncompleteException(f"Output Data Label with reason extension not found")

    def __generate_reason_tag(self, additional_label: str, current_reason: Optional[str]) -> Optional[str]:
        self.__logger.debug(f"generate reason tag")
        self.__logger.debug(f"additional_label -> {additional_label}")
        self.__logger.debug(f"current_reason -> {current_reason}")
        if current_reason is not None:
            self.__logger.debug(f"current reason is not None")
            structed_additional_label: DtoLabel = self.__LabelParser.struct(additional_label)
            structed_current_reason: DtoLabel = self.__LabelParser.struct(current_reason)
            self.__logger.debug(f"current reason is not None")
            new_reason: str = ("{" +
                               structed_current_reason.getLabelName() + structed_current_reason.getLabelSign() +
                               structed_additional_label.getLabelName() + "->" + structed_additional_label.getLabelValue() + "; "
                               + structed_current_reason.getLabelValue()
                               + "}")
            self.__logger.debug(f"new reason is set: {new_reason}")
            return new_reason
        else:
            return None

    def __merge_reasons(self, reason_tag_list: list[str]) -> Optional[str]:
        final_reason: Optional[str] = None
        if reason_tag_list == []:
            return None
        for reason in reason_tag_list:
            if final_reason is not None:
                structed_reason: DtoLabel = self.__LabelParser.struct(reason)
                final_reason = final_reason + "; " + structed_reason.getLabelValue()
            else:
                structed_reason: DtoLabel = self.__LabelParser.struct(reason)
                final_reason = structed_reason.getLabelValue()
        final_reason_tag = "{reason=" + final_reason + "}"
        return final_reason_tag

    def __get_reason_tag(self, list_tags: list[str]) -> str:
        self.__logger.debug(f"Search for reason tag")
        tag: Optional[str] = None
        for tag in list_tags:
            structed_tag: DtoLabel = self.__LabelParser.struct(tag)
            if structed_tag.getLabelName() == "reason":
                tag = self.__LabelParser.destruct(structed_tag)
        if tag is not None:
            return tag
        else:
            return "reason=ERR:REASON_TAG_NOT_FOUND"

    def __get_output_node_label(self):
        self.__logger.debug(f"Search for OutputDataLabel")
        output_node_label: Optional[str] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputDataLabel" and abstract_data.get_abstract_data_key() == "label":
                output_node_label = abstract_data.get_abstract_data_value()
                break
        if output_node_label is not None:
            return output_node_label
        else:
            raise Exceptions.OperationIncompleteException(f"Output Data Label not found")

    def __get_output_data_name(self) -> str:
        output_data_name: Optional[str] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputData":
                output_data_name = abstract_data.get_abstract_data_specialty()
                break
        if output_data_name is not None:
            return output_data_name
        else:
            raise Exceptions.OperationIncompleteException(f"Output data not found")

    def __get_output_data_key(self) -> str:
        output_data_key: Optional[str] = None
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "OutputData":
                output_data_key = abstract_data.get_abstract_data_key()
                break
        if output_data_key is not None:
            return output_data_key
        else:
            raise Exceptions.OperationIncompleteException(f"Output data not found")

    def __get_raw_data_list(self, input_storage: i_Storage) -> list[StorageItem]:
        raw_data_list: list[Optional[i_StorageItem, StorageItem]] = []
        for abstract_data in self._abstract_data_list:
            if abstract_data.get_abstract_data_type() == "InputData":
                self.__logger.debug(f"input data id is {abstract_data.get_abstract_data_specialty()}")
                raw_data_list.append(input_storage.read(abstract_data.get_abstract_data_specialty()))
        return raw_data_list

    def __get_input_storage(self) -> i_Storage:
        input_storage_name: Optional[str] = self.__get_input_storage_name()
        input_storage: i_Storage = self._storage_manager.get_storage(input_storage_name, self._current_node_description)
        self.__logger.debug(f"input storage received")
        return input_storage

    def __get_output_storage(self) -> i_Storage:
        output_storage_name: Optional[str] = self.__get_output_storage_name()
        output_storage: i_Storage = self._storage_manager.get_storage(output_storage_name, self._current_node_description)
        self.__logger.debug(f"output storage received")
        return output_storage

    def __get_input_storage_name(self) -> str:
        input_storage_name: Optional[str] = None
        for configuration in self._configuration_list:
            if configuration.get_abstract_data_type() == "InputStorage":
                input_storage_name = configuration.get_abstract_data_specialty()
                break
        if input_storage_name is not None:
            return input_storage_name
        else:
            raise Exceptions.OperationIncompleteException(f"Input storage not found")

    def __get_output_storage_name(self) -> str:
        output_storage_name: Optional[str] = None
        for configuration in self._configuration_list:
            if configuration.get_abstract_data_type() == "OutputStorage":
                output_storage_name = configuration.get_abstract_data_specialty()
                break
        if output_storage_name is not None:
            return output_storage_name
        else:
            raise Exceptions.OperationIncompleteException(f"Output storage not found")

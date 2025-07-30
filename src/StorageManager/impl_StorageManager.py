#
#
#
import logging
from i_Storage import i_Storage
from .impl_Storage import impl_Storage
from LibByzaticCommon import Exceptions
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceStorages import NodeUnitWorkersPipelineStagesGlobalSpaceStorages
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions import NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions
from Global2p2.i_StorageManager import i_StorageManager
from Global.NodeUnitDescription import NodeUnitDescription
from .ManagerStorage import ManagerStorage
from typing import Optional


class impl_StorageManager(i_StorageManager):
    def __init__(self, storage_manager_configuration_list: list[NodeUnitWorkersPipelineStagesGlobalSpaceStorages], nodes_description_list: list[NodeUnitDescription]):
        self.__logger: logging.Logger = logging.getLogger("StorageManager-logger")
        self.__ManagerStorage: ManagerStorage = ManagerStorage("ManagerStorage-storage")
        self.__storage_manager_configuration_list: list[NodeUnitWorkersPipelineStagesGlobalSpaceStorages] = storage_manager_configuration_list
        self.__nodes_description_list: list[NodeUnitDescription] = nodes_description_list
        self.__init_storages()

    def __init_storages(self) -> None:
        try:
            for storage_manager_configuration in self.__storage_manager_configuration_list:
                storage_name: str = storage_manager_configuration.get_id_name()
                logger_name_of_storage: str = f"{storage_name}-logger"
                storage_link: str = self.__get_node_link(storage_manager_configuration.get_options(), storage_name)
                if storage_link == "node":
                    node_id_list: list[str] = self.__get_descriptions_str_list()
                    for node_id in node_id_list:
                        new_storage_name = f"{storage_name}{node_id}"
                        self.__ManagerStorage.create(new_storage_name, impl_Storage(logger_name_of_storage))
                        self.__logger.debug(f"Created storage -> {new_storage_name}")
                elif storage_link == "NoneLinked":
                    self.__ManagerStorage.create(storage_name, impl_Storage(logger_name_of_storage))
                    self.__logger.debug(f"Created storage -> {storage_name}")
                else:
                    raise Exceptions.OperationIncompleteException(f"Invalid value of storage parameter name -> {storage_link}")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __get_node_link(self, storage_options: list[NodeUnitWorkersPipelineStagesGlobalSpaceStoragesOptions], storage_name: str) -> str:
        search_state: bool = False
        search_result: str = ""
        for storage_option in storage_options:
            if storage_option.get_name() == "link":
                search_state = True
                search_result = storage_option.get_data()
        if search_state is True:
            return search_result
        else:
            raise Exceptions.OperationIncompleteException(f"link parameter is not set for storage {storage_name}")

    def __get_descriptions_str_list(self) -> list[str]:
        node_id_list: list[str] = []
        for nodes_description in self.__nodes_description_list:
            node_id = nodes_description.get_node_id()
            node_id_list.append(node_id)
        return node_id_list

    def __create_storage(self, storage_name: str):
        logger_name_of_storage: str = f"{storage_name}-logger"
        self.__ManagerStorage.create(storage_name, impl_Storage(logger_name_of_storage))

    def get_storage(self, storage_name: str, nodeunit_description: Optional[NodeUnitDescription] = None) -> i_Storage:
        try:
            self.__logger.debug(f"Getting storage")
            combined_storage_name: str
            if nodeunit_description is not None:
                combined_storage_name = f"{storage_name}{nodeunit_description.get_node_id()}"
                self.__logger.debug(f"node unit description is set; requested storage name is {combined_storage_name}")
            else:
                combined_storage_name = f"{storage_name}"
                self.__logger.debug(f"node unit description is not set; requested storage name is {combined_storage_name}")
            storage: i_Storage = self.__ManagerStorage.read(combined_storage_name)
            return storage
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def remove_storage(self, storage_name: str, nodeunit_description: Optional[NodeUnitDescription] = None) -> None:
        try:
            self.__logger.debug(f"Removing storage")
            combined_storage_name: str
            if nodeunit_description is not None:
                combined_storage_name = f"{storage_name}{nodeunit_description}"
                self.__logger.debug(f"node unit description is set; requested storage name is {combined_storage_name}")
            else:
                combined_storage_name = f"{storage_name}"
                self.__logger.debug(f"node unit description is not set; requested storage name is {combined_storage_name}")
            self.__ManagerStorage.delete(combined_storage_name)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def put_storage(self, storage_name: str, storage_unit: i_Storage, nodeunit_description: Optional[NodeUnitDescription] = None) -> None:
        try:
            self.__logger.debug(f"Saving storage")
            combined_storage_name: str
            if nodeunit_description is not None:
                combined_storage_name = f"{storage_name}{nodeunit_description.get_node_id()}"
                self.__logger.debug(f"node unit description is set; requested storage name is {combined_storage_name}")
            else:
                combined_storage_name = f"{storage_name}"
                self.__logger.debug(f"node unit description is not set; requested storage name is {combined_storage_name}")
            if self.__ManagerStorage.contains(combined_storage_name):
                self.__ManagerStorage.delete(combined_storage_name)
                self.__ManagerStorage.create(combined_storage_name, storage_unit)
            else:
                self.__ManagerStorage.create(combined_storage_name, storage_unit)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def recreate_storages(self) -> None:
        try:
            self.__ManagerStorage.drop()
            self.__init_storages()
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

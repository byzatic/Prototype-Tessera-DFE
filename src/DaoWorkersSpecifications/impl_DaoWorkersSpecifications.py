#
#
#
import logging
from Global2p2.i_DaoWorkersSpecifications import i_DaoWorkersSpecifications
from marshmallow import RAISE
from Global2p2.WorkerSpecification.WorkerSpecification import WorkerSpecification
from .MrshmellowModels.SchemaWorkerSpecification import SchemaWorkerSpecification
from LibByzaticCommon.FileReaders import JsonFileReader, BaseReaderInterface
from .impl_WorkerSpecificationStorage import impl_WorkerSpecificationStorage
from .i_WorkerSpecificationStorage import i_WorkerSpecificationStorage
from LibByzaticCommon import Exceptions


class impl_DaoWorkersSpecifications(i_DaoWorkersSpecifications):
    def __init__(self, data_file: str):
        self.__logger: logging.Logger = logging.getLogger("DaoWorkersSpecifications-logger")
        self.__data_file: str = data_file
        self.__JsonFileReader: BaseReaderInterface = JsonFileReader()
        self.__WorkerSpecificationStorage: i_WorkerSpecificationStorage = impl_WorkerSpecificationStorage("WorkerSpecificationStorage-storage")
        self.__SchemaWorkerSpecification: SchemaWorkerSpecification = SchemaWorkerSpecification()
        self.__create_preloaded_data()

    def __create_preloaded_data(self):
        try:
            dict_json_data: list = self.__JsonFileReader.read(self.__data_file)
            for data_item in dict_json_data:
                worker_specification_instance: WorkerSpecification = self.__SchemaWorkerSpecification.load(data=data_item, unknown=RAISE)
                storage_id: str = worker_specification_instance.get_name()
                self.__WorkerSpecificationStorage.create(storage_id, worker_specification_instance)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def get_worker_specification(self, worker_specification_name: str) -> WorkerSpecification:
        try:
            if self.__WorkerSpecificationStorage.contains(worker_specification_name):
                return self.__WorkerSpecificationStorage.read(worker_specification_name)
            else:
                err_description: str = f"workers' specification for worker with name {worker_specification_name} not found"
                self.__logger.error(err_description)
                self.__logger.error(f"List available workers' specification by worker name: {self.__WorkerSpecificationStorage.read_list_keys()}")
                raise Exceptions.OperationIncompleteException(err_description)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)


#
#
#
import logging
from typing import Optional
from WorkersManager.local_api.i_PiplineManager import i_PiplineManager
from Global2p1.NodeUnit.NodeUnitWorkersPipeline import NodeUnitWorkersPipeline
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesConsistency import NodeUnitWorkersPipelineStagesConsistency
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageInfo import NodeUnitWorkersPipelineStagesDescriptionStageInfo
from Global2p1.NodeUnit.NodeUnitWorkersPipelineStagesDescriptionStageData import NodeUnitWorkersPipelineStagesDescriptionStageData
from LibByzaticCommon import Exceptions
from copy import deepcopy


class impl_PiplineManager(i_PiplineManager):
    def __init__(self):
        self.__logger: logging.Logger = logging.getLogger("WorkersManager-PiplineManager-logger")

    def make_pipline(self, node_unit_workers_pipeline: NodeUnitWorkersPipeline) -> list[NodeUnitWorkersPipelineStagesDescriptionStageData]:
        try:
            self.__logger.debug(f"Try to crate pipline")

            self.__logger.debug(f"extraction of stages consistency list")
            pipline_stages_consistency_list: list[NodeUnitWorkersPipelineStagesConsistency] = node_unit_workers_pipeline.get_stages_consistency()
            self.__logger.debug(f"extracted stages consistency list")

            self.__logger.debug(f"sorting of stages consistency list")
            sorted_stages_consistency_list: list[NodeUnitWorkersPipelineStagesConsistency] = self.__make_sort_stages_consistency(pipline_stages_consistency_list)
            self.__logger.debug(f"sorted stages consistency list")

            self.__logger.debug(f"extracting of stages info list")
            pipline_stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo] = node_unit_workers_pipeline.get_stages_description().get_stages_info()
            self.__logger.debug(f"extracted stages info list")

            self.__logger.debug(f"sorting of stages info list")
            sorted_pipline_stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo] = self.__make_sort_pipline_stages_info_by_sorted_stages_consistency_list(pipline_stages_info_list, sorted_stages_consistency_list)
            self.__logger.debug(f"sorted stages info list")

            self.__logger.debug(f"creating of job data list")
            sorted_pipline_job_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageData] = self.__make_sort_pipline_job_data_list(sorted_pipline_stages_info_list)
            self.__logger.debug(f"created job data list")

            self.__logger.debug(f"final pipline is {len(sorted_pipline_job_data_list)} elements")
            self.__logger.debug(f"crate pipline complete")
            return sorted_pipline_job_data_list
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __make_sort_pipline_job_data_list(self, sorted_pipline_stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo]) -> list[NodeUnitWorkersPipelineStagesDescriptionStageData]:
        try:
            self.__logger.debug(f"Try to make sorted pipline job data list")
            sorted_pipline_job_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageData] = []
            for sorted_pipline_stages_info_item in sorted_pipline_stages_info_list:
                pipline_job_data_list: list[NodeUnitWorkersPipelineStagesDescriptionStageData] = sorted_pipline_stages_info_item.get_stage_data()
                self.__logger.debug(f"extend final pipline job data list with {len(pipline_job_data_list)} elements")
                sorted_pipline_job_data_list.extend(pipline_job_data_list)
            self.__logger.debug(f"complete to make sorted pipline job data list")
            return deepcopy(sorted_pipline_job_data_list)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __make_sort_pipline_stages_info_by_sorted_stages_consistency_list(self, pipline_stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo], sorted_stages_consistency_list: list[NodeUnitWorkersPipelineStagesConsistency]) -> list[NodeUnitWorkersPipelineStagesDescriptionStageInfo]:
        try:
            self.__logger.debug(f"Try to sort pipline stages info list of {len(pipline_stages_info_list)} items by sorted stages consistency list of {len(sorted_stages_consistency_list)} items")
            self.__logger.debug(f"pipline stages consistency list -> {sorted_stages_consistency_list}")
            self.__logger.debug(f"pipline stages info list -> {pipline_stages_info_list}")
            sorted_pipline_stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo] = []
            for sorted_stages_consistency_item in sorted_stages_consistency_list:
                sorted_stages_consistency_name: str = sorted_stages_consistency_item.get_name()
                self.__logger.debug(f"extract sorted stages item consistency name -> {sorted_stages_consistency_name}")
                list_all_pipline_stages_info_by_stage_name: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo] = self.__get_list_all_pipline_stages_info_by_stage_name(sorted_stages_consistency_name, pipline_stages_info_list)
                self.__logger.debug(f"extend final result with {len(list_all_pipline_stages_info_by_stage_name)} items")
                sorted_pipline_stages_info_list.extend(list_all_pipline_stages_info_by_stage_name)
            self.__logger.debug(f"complete to sort pipline stages info list, result is {len(sorted_pipline_stages_info_list)} elements")
            return deepcopy(sorted_pipline_stages_info_list)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __get_list_all_pipline_stages_info_by_stage_name(self, stage_name: str, pipline_stages_info_list: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo]) -> list[NodeUnitWorkersPipelineStagesDescriptionStageInfo]:
        list_all_pipline_stages_info: list[NodeUnitWorkersPipelineStagesDescriptionStageInfo] = []
        self.__logger.debug(f"Try to get list of all pipline stages info by stage name {stage_name}")
        for pipline_stages_info_item in pipline_stages_info_list:
            if pipline_stages_info_item.get_stage_id() == stage_name:
                list_all_pipline_stages_info.append(pipline_stages_info_item)
        self.__logger.debug(f"found {len(list_all_pipline_stages_info)} elements of pipline stage {stage_name}")
        return list_all_pipline_stages_info

    def __make_sort_stages_consistency(self, pipline_stages_consistency_list: list[NodeUnitWorkersPipelineStagesConsistency]) -> list[NodeUnitWorkersPipelineStagesConsistency]:
        try:
            self.__logger.debug(f"Try to sort stages consistency list of {len(pipline_stages_consistency_list)} items")
            list_stages_consistency: list[NodeUnitWorkersPipelineStagesConsistency] = []
            list_stages_consistency_positions: list[int] = []
            for worker_info_item in pipline_stages_consistency_list:
                worker_position: str = worker_info_item.get_position()
                self.__logger.debug(f"extracted position {worker_position}")
                int_worker_position: int = int(worker_position)
                list_stages_consistency_positions.append(int_worker_position)
            self.__logger.debug(f"extracted positions list {str(list_stages_consistency_positions)}")
            self.__insertion_sort(list_stages_consistency_positions)
            self.__logger.debug(f"extracted positions list after insertion sort {str(list_stages_consistency_positions)}")
            self.__logger.debug(f"check duplicated items")
            self.__check_dup(list_stages_consistency_positions)
            self.__logger.debug(f"check duplicated items complete")
            self.__logger.debug(f"check consecutive")
            self.__check_consecutive(list_stages_consistency_positions)
            self.__logger.debug(f"check consecutive complete")
            for stages_consistency_item in list_stages_consistency_positions:
                self.__logger.debug(f"search pipline stages consistency item by position")
                pipline_stages_consistency_item: NodeUnitWorkersPipelineStagesConsistency = self.__search_pipline_stages_consistency_item(stages_consistency_item, pipline_stages_consistency_list)
                self.__logger.debug(f"add pipline stages consistency item {pipline_stages_consistency_item} to the final list")
                list_stages_consistency.append(pipline_stages_consistency_item)
            self.__logger.debug(f"return the final list of pipline stages consistency item")
            self.__logger.debug(f"complete to sort stages consistency list of {len(pipline_stages_consistency_list)} items")
            return deepcopy(list_stages_consistency)
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __search_pipline_stages_consistency_item(self, searching_position: int, pipline_stages_consistency_list: list[NodeUnitWorkersPipelineStagesConsistency]) -> NodeUnitWorkersPipelineStagesConsistency:
        try:
            self.__logger.debug(f"search pipline stages consistency item by position {searching_position}")
            deepcopy_pipline_stages_consistency_item: Optional[NodeUnitWorkersPipelineStagesConsistency] = None

            for pipline_stages_consistency_item in pipline_stages_consistency_list:
                if str(searching_position) == str(pipline_stages_consistency_item.get_position()):
                    self.__logger.debug(f"found pipline stages consistency item {pipline_stages_consistency_item} by position {searching_position}")
                    deepcopy_pipline_stages_consistency_item = deepcopy(pipline_stages_consistency_item)
                    self.__logger.debug(f"pipline stages consistency item deepcopy -> {deepcopy_pipline_stages_consistency_item}")
                    break
                else:
                    self.__logger.debug(f"searching position {searching_position} is not {pipline_stages_consistency_item.get_position()}")
            if deepcopy_pipline_stages_consistency_item is not None:
                return deepcopy_pipline_stages_consistency_item
            else:
                raise Exceptions.OperationIncompleteException(f"NodeUnitWorkersPipelineStagesConsistency with position {searching_position} not found in list of NodeUnitWorkersPipelineStagesConsistency")
        except Exceptions.OperationIncompleteException as oie:
            raise Exceptions.OperationIncompleteException(oie.args, errno=oie.errno)
        except Exception as e:
            raise Exceptions.OperationIncompleteException(e.args)

    def __insertion_sort(self, arr: list[int]) -> None:
        self.__logger.debug(f"Run insertion sort for {arr}")
        for i in range(1, len(arr)):
            key = arr[i]
            j: int = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        self.__logger.debug(f"Finish insertion sort with {arr}")

    def __check_dup(self, arr: list[int]) -> None:
        visited = set()
        dup: list[int] = [x for x in arr if x in visited or (visited.add(x) or False)]
        if dup:
            raise Exceptions.OperationIncompleteException(f"PiplineManager: Pipline error: found duplicated codes: {str(dup)}")

    def __check_consecutive(self, arr: list[int]) -> None:
        if self.__is_consecutive(arr):
            self.__logger.debug(f"Pipline is consecutive")
        else:
            self.__logger.warning(f"Pipline error: Pipline is not consecutive")

    def __is_consecutive(self, arr: list[int]) -> bool:
        if len(arr) <= 1:
            return True
        minimum = min(arr)
        maximum = max(arr)
        if maximum - minimum != len(arr) - 1:
            return False
        visited = set()
        for i in arr:
            if i in visited:
                return False
            visited.add(i)
        return True

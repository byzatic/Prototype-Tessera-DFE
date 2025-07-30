#!/usr/bin/env python3
#
# ========= Interfaces =========
#
#
#
#
from abc import ABCMeta, abstractmethod
from Global2p2.WorkerSpecification import WorkerSpecification


class i_WorkerSpecificationStorage():
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, key: str, value: WorkerSpecification) -> None:
        pass

    @abstractmethod
    def read(self, key: str) -> WorkerSpecification:
        pass

    @abstractmethod
    def update(self, key: str, value: WorkerSpecification) -> int:
        pass

    @abstractmethod
    def delete(self, key: str) -> int:
        pass

    @abstractmethod
    def drop(self) -> int:
        pass

    @abstractmethod
    def read_all(self) -> WorkerSpecification:
        pass

    @abstractmethod
    def read_list_keys(self) -> list:
        pass

    @abstractmethod
    def contains(self, key: str) -> bool:
        pass

from abc import ABC, abstractmethod
from typing import List
from src.sync_tmp_events.extract.contracts.IAbstractDTO import IAbstractDTO


class LoadFacadeABC(ABC):

    def __init__(self) -> None:
        self.data_to_notify: List                                                                       [IAbstractDTO] = []
    
    @abstractmethod
    async def load_fact(self, data_to_load: List[IAbstractDTO]) -> None:
        raise NotImplementedError
    

    @abstractmethod
    async def delete_events(self, data_to_delete: List[IAbstractDTO]) -> None:
        raise NotImplementedError


    @abstractmethod
    async def notify_changes(self) -> None:
        raise NotImplementedError
from abc import ABC, abstractmethod
from typing import List
from src.sync_tmp_events.extract.contracts.IAbstractDTO import IAbstractDTO



class TransformFacadeABC(ABC):

    def __init__(self) -> None:
        self.data_to_transform: List[IAbstractDTO] = []
        self.data_to_delete: List[IAbstractDTO] = []

    @abstractmethod
    async def transform_fact_to_sync(self, data_to_transform: List[IAbstractDTO]) -> List[IAbstractDTO]:
        raise NotImplementedError
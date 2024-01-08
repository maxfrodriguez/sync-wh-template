from abc import ABC, abstractmethod
import asyncio
from typing import List

from src.sync_tmp_events.extract.contracts.IAbstractDTO import IAbstractDTO
from common.common_infrastructure.cross_cutting.ConfigurationEnvHelper import ConfigurationEnvHelper

class ExtractFacadeABC:

    def __init__(self) -> None:
        # self.wh_repository = None
        # self.pt_repository = None
        self.data_to_sync: List[IAbstractDTO] = []
        self.reference_ids_to_sync: set = set()
        self._pack_size: int = 0

    @abstractmethod
    def get_fact_information(self, reference_data : list[dict] = None) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def next_fact_to_sync(self, pack_size):
        raise NotImplementedError
    
    async def set_pack_size(self):
        if len(self.data_to_sync) > 0:
            vault_pack_size = await ConfigurationEnvHelper().get_secret("PackageSizeToSync")
            if (vault_pack_size 
                and vault_pack_size.isdigit()
                and int(vault_pack_size) < len(self.data_to_sync)):
                self._pack_size = int(vault_pack_size)
            else:
                self._pack_size = len(self.data_to_sync)

    
    #this method retrieve the data to sync in pack_size
    def next_fact_to_sync(self) -> List[IAbstractDTO]:
        for i in range(0, len(self.data_to_sync), self._pack_size):
            yield self.data_to_sync[i : i + self._pack_size]
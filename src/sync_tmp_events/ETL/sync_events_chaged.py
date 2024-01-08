import logging
from typing import Any, Dict, List
from src.sync_tmp_events.load.contracts.facade_load_abc import LoadFacadeABC


from src.sync_tmp_events.extract.contracts.facade_extract_abc import ExtractFacadeABC
from src.sync_tmp_events.transform.contracts.facade_transform_abc import TransformFacadeABC


class SyncronizerChagesInFact:
    def __init__(self
                 , extract_service: ExtractFacadeABC
                 , transform_service: TransformFacadeABC
                 , load_service : LoadFacadeABC) -> None:
        self.extract_facade = extract_service
        self.transform_facade = transform_service
        self.load_facade = load_service
        self._ids_with_error : str = ""

    async def syncronize_fact(self, reference_data : List[Dict[str, Any]] = None) -> None:
        
        # convert the tmps_changed to shipment_changed
        # if reference_data:
        #     self.shipments_changed = [ShipmentsChangedExample(**tmp) for tmp in reference_data]

        await self.extract_facade.get_fact_information(None)
    
        # sincronize all if has less than 200 events to sync
        try:
            await self.extract_facade.set_pack_size()
            for data_to_sync in self.extract_facade.next_fact_to_sync():
                try:
                    await self.transform_facade.transform_fact_to_sync(data_to_sync)
                    
                    await self.load_facade.load_fact(self.transform_facade.data_to_transform)
                    #await self.load_facade.delete_events(self.transform_facade.event_to_delete)

                    await self.load_facade.notify_changes()

                except Exception as e:
                    ids = ", ".join(f"'{shipment.ds_id}'" for shipment in data_to_sync)
                    logging.error(f"Error in syncronize shipments: {ids} with error: {e}")
                    self._ids_with_error += ids

            # if self._ids_with_error:
            #     raise Exception(f"Error in syncronize shipments: {self._ids_with_error}")
                
        except Exception as e:
            logging.error(f"Error in syncronize shipments: {e}")
            raise e


    # async def notify(self, events_to_notify):
    #     notify_manager = NotifierManager()

    #     notify_manager.register_notifier(EventChangedNotifier())

    #     await notify_manager.notify_all_by_pakages(events_to_notify, size_pagake=10)
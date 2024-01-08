import logging
from typing import Any, Dict, List
from os import getenv
from orjson import dumps

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from common.common_infrastructure.cross_cutting.ConfigurationEnvHelper import ConfigurationEnvHelper
from src.sync_tmp_events.ETL.notifier_abc import Notifier
from src.sync_tmp_events.extract.data.ExampleDTO import ExampleDTO

class EventChangedNotifier(Notifier):
    def __init__(self) -> None:
        self._secret: dict[str, str] = {
            "conn": "ServiceBusConn",
            "topic": "SbTopicEventToSync",
            "subscription": "SbSubscriptionEventToSync"
        }
        self._sb_client: ServiceBusClient = None

    async def __connect(self):
        self._secret = await ConfigurationEnvHelper().get_secrets(self._secret)
        self._sb_client = ServiceBusClient.from_connection_string(conn_str=self._secret["conn"])

    async def send_information(self, list_events: List[ExampleDTO]):
        if not self._sb_client:
            await self.__connect()

        try:
            events : List[Dict[str, Any]] = []
            for event in list_events:
                events.append({
                    "de_id": event.de_id
                    , "ds_id": event.ds_id
                    })
            
            sender = self._sb_client.get_topic_sender(topic_name=self._secret["topic"], subscription_name=self._secret["subscription"])
            message = ServiceBusMessage(dumps(events))
            sender.send_messages(message)

        except Exception as e:
            logging.error(f"Error in send_customer_kpi_sb: {e}")
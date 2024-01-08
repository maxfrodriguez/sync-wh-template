import logging


from common.common_infrastructure.dataaccess.db_context.sybase.sql_anywhere_impl import SQLAnywhereBase


class PTSQLAnywhere(SQLAnywhereBase):
    def __init__(self):
        secrets = {"uid": "PtUid", "pwd": "PtPwd", "host": "PtHost", "dbn": "PtDbn", "server": "PtServer"}
        super().__init__(keyVaults=secrets)

    async def connect(self) -> None:
        try:
            await self._get_credentials()
            await self._get_sybase_resources()
        except Exception as e:
            logging.error(f"Error connecting to database 121Tower: {e}")
            raise e

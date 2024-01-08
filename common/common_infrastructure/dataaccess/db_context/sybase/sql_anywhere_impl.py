import logging
from collections import namedtuple
from typing import Any, Dict, Generator, List, Tuple, Type, TypeVar

from sqlanydb import Connection, Cursor, connect
from typing_extensions import Self

from common.common_infrastructure.cross_cutting.ConfigurationEnvHelper import ConfigurationEnvHelper

from .sql_anywhere_abc import SQLAnywhereABC

Record = TypeVar("Record", bound=tuple)


class SQLAnywhereBase(SQLAnywhereABC):
    _instance = None
    _secrets: Dict[str, str] = None
    _connection: Connection = None
    _cursor: Cursor = None
    _keyVaultParams: Dict[str, str] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, keyVaults: dict[str, str] = None) -> None:
        self._keyVaultParams = keyVaults

    async def _get_credentials(self) -> Dict[str, str]:
        if self._secrets is None:
            self._secrets = {}
        
        self._secrets = await ConfigurationEnvHelper().get_secrets(self._keyVaultParams)

    async def _get_sybase_resources(self) -> None:
        self._connection = connect(uid=self._secrets["uid"]
                                   , pwd=self._secrets["pwd"]
                                   , host=self._secrets["host"]
                                   , dbn=self._secrets["dbn"]
                                   , server=self._secrets["server"])
        # get sessionmaker from connection
        self._cursor = self._connection.cursor()

    async def close_all(self) -> None:
        try:
            self._cursor.close()
            self._connection.close()
        except Exception as e:
            logging.exception(f"An exception has occurred. {str(e)}")

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *_) -> None:
        await self.close_all()

    def __generator_dict_fetch_all(self) -> Generator[Dict, None, None]:
        "Return all rows from a cursor as a dict"
        columns: List[str] = [col[0] for col in self._cursor.description]
        return (dict(zip(columns, row)) for row in self._cursor.fetchall())

    def __generator_named_tuple_fetch_all(self) -> Generator[Record, None, None]:
        "Return all rows from a cursor as a namedtuple"
        desc = self._cursor.description
        nt_result = namedtuple("Record", [col[0] for col in desc])
        return (nt_result(*row) for row in self._cursor.fetchall())

    def __fetch_all(self, result_type: Type = dict) -> List[Dict[str, Any] | Record]:
        desc = self._cursor.description
        nt_result = namedtuple("Record", [col[0] for col in desc])
        columns: List[str] = [col[0] for col in desc]
        if result_type is dict:
            return [dict(zip(columns, row)) for row in self._cursor.fetchall()]
        elif result_type is nt_result:
            return [nt_result(*row) for row in self._cursor.fetchall()]
        else:
            raise ValueError(f"Invalid result type: {result_type}")

    def SELECT(self, query: str, result_type: Type = dict) -> Generator[Dict | Record, None, None]:
        result: Generator[Dict | Record, None, None] = None
        try:
            self._cursor.execute(query)
            if result_type is dict:
                result = self.__fetch_all()
            elif result_type is namedtuple:
                result = self.__generator_named_tuple_fetch_all()
            else:
                raise ValueError(f"Invalid result type: {result_type}")
        except Exception as e:
            logging.exception(f"An exception has occurred. {str(e)}")
        finally:
            return result

    def SELECT_ONE(self, query: str) -> Tuple | None:
        result: Tuple | None = None
        try:
            self._cursor.execute(query)
        except Exception as e:
            logging.exception(f"An exception has occurred. {str(e)}")
        else:
            result = self._cursor.fetchone()
        finally:
            return result

    @property
    def cursor(self) -> Cursor:
        return self._cursor

from abc import abstractmethod

class SQLAnywhereABC():
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def close_all(self) -> None:
        raise NotImplementedError

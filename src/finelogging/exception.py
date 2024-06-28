import asyncio
import traceback
from abc import ABC, abstractmethod
from typing import Any, Optional

from .logger import Level, get_logger

logger = get_logger()


class BaseFineException(ABC, Exception):
    """Base class for all exceptions in the fine logging library."""

    level: Level = Level.WARNING
    message: Optional[str] = None

    def __init__(
        self, msg: Optional[str] = None, log: bool = True, **kwargs: Any
    ) -> None:
        self._msg, self._kwargs = self.handle_log(msg or self.message, **kwargs)
        super().__init__(self._msg)

        if log:
            self._log_exception(self._msg, self._kwargs)

    @abstractmethod
    def handle_log(self, msg: Optional[str] = None, **kwargs: Any) -> tuple[str, dict[str, Any]]: ...

    @abstractmethod
    def _log_exception(self, msg: str, kwargs: dict[str, Any]) -> None: ...


class FineException(BaseFineException):
    """Exception for fine logging library."""

    def _log_exception(self, msg: str, kwargs: dict[str, Any]) -> None:
        logger.log(self.level, msg, **kwargs)

    def handle_log(self, msg: Optional[str] = None, **kwargs: Any) -> tuple[str, dict[str, Any]]:
        return (
            msg or self.__class__.__name__,
            {
                **kwargs,
                "exception_class": self.__class__.__name__,
                "exc_info": self,
                "stacktrace": traceback.format_exc(),
            },
        )


class FineAsyncException(FineException):
    """Async exception for fine logging library."""

    def _log_exception(self, msg: str, kwargs: dict[str, Any]) -> None:
        asyncio.create_task(logger.alog(self.level, msg, **kwargs))

    @classmethod
    async def raise_exc(
        cls, msg: Optional[str] = None, log: bool = True, **kwargs: Any
    ) -> None:
        """Raise an async exception."""

        exception = cls(msg, False, **kwargs)
        if log:
            await logger.alog(cls.level, exception._msg, **exception._kwargs)
        raise exception

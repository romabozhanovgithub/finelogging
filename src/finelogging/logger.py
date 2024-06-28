import logging
from enum import IntEnum
from typing import Callable, Optional

import structlog


class Level(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)


def _configure_base_logger(level: Level) -> None:
    base_logger = logging.getLogger()
    base_logger.setLevel(level.value)
    base_logger.addHandler(logging.StreamHandler())


def configure_logging(
    level: Level = Level.INFO,
    fmt: str = "%Y-%m-%d %H:%M:%S",
    wrapper_class: type[structlog.typing.BindableLogger] = structlog.stdlib.BoundLogger,
    logger_factory: Callable[..., structlog.stdlib.WrappedLogger] = structlog.stdlib.LoggerFactory,
) -> None:
    _configure_base_logger(level)
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt=fmt),
            structlog.processors.EventRenamer("msg"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=wrapper_class,
        logger_factory=logger_factory(),
        cache_logger_on_first_use=True,
    )

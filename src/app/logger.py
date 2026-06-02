import sys
from pathlib import Path
from typing import TextIO

import structlog


def _build_stream(log_file: str | Path | None) -> TextIO:
    if log_file is None:
        return sys.stdout

    return Path(log_file).open("a", encoding="utf-8")


def configure_logger(log_file: str | Path | None = None) -> structlog.BoundLogger:
    structlog.reset_defaults()
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.add_log_level,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(0),
        logger_factory=structlog.WriteLoggerFactory(file=_build_stream(log_file)),
        cache_logger_on_first_use=False,
    )
    return structlog.get_logger("log_analyzer")

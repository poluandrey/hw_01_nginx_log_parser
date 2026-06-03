import gzip
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, TextIO

LOG_FILE_PATTERN = re.compile(
    r"^nginx-access-ui\.log-(?P<date>\d{8})(?P<extension>\.gz)?$",
)


@dataclass(frozen=True)
class LogFileInfo:
    path: Path
    log_date: datetime
    extension: str


def _match_log_file(log_path: Path) -> LogFileInfo | None:
    match = LOG_FILE_PATTERN.match(log_path.name)
    if match is None:
        return None

    return LogFileInfo(
        path=log_path,
        extension=match.group("extension") or "",
        log_date=datetime.strptime(match.group("date"), "%Y%m%d"),
    )


def _iter_log_files(log_dir: str | Path) -> Iterator[LogFileInfo]:
    log_dir_path = Path(log_dir)
    if not log_dir_path.exists():
        return

    for log_path in log_dir_path.iterdir():
        if not log_path.is_file():
            continue

        matched_log = _match_log_file(log_path)
        if matched_log is not None:
            yield matched_log


def find_latest_log(log_dir: str | Path) -> LogFileInfo | None:
    return max(
        _iter_log_files(log_dir),
        default=None,
        key=lambda log_file: log_file.log_date,
    )


def _open_log_stream(log_file: LogFileInfo) -> TextIO:
    if log_file.extension == ".gz":
        return gzip.open(log_file.path, "rt", encoding="utf-8")

    return log_file.path.open("r", encoding="utf-8")


def parse_log_line(line: str) -> tuple[str, float] | None:
    line_parts = line.split('"')
    if len(line_parts) < 2:
        return None

    request_parts = line_parts[1].split()
    if len(request_parts) < 2:
        return None

    request_time = line_parts[-1].strip()
    if not request_time:
        return None

    return request_parts[1], float(request_time)


def iter_log_records(log_file: LogFileInfo) -> Iterator[tuple[str, float]]:
    with _open_log_stream(log_file) as log_stream:
        for line in log_stream:
            parsed_line = parse_log_line(line)
            if parsed_line is not None:
                yield parsed_line

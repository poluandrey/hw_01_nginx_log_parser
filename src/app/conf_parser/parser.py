from pathlib import Path
from typing import Any

from app.config import config

Config = dict[str, Any]


def _parse_config_line(line: str) -> tuple[str, str] | None:
    stripped_line = line.strip()
    if not stripped_line or stripped_line.startswith("#") or "=" not in stripped_line:
        return None

    key, raw_setting = stripped_line.split("=", 1)
    return key.strip(), raw_setting.strip()


def _parse_config_value(config_key: str, raw_setting: str) -> Any:
    if config_key == "REPORT_SIZE":
        return int(raw_setting)
    return raw_setting


def _merge_config_line(parsed_config: Config, line: str) -> None:
    parsed_line = _parse_config_line(line)
    if parsed_line is None:
        return

    config_key, raw_setting = parsed_line
    if not raw_setting:
        return

    parsed_config[config_key] = _parse_config_value(config_key, raw_setting)


def parse_config(file_path: str | Path | None = None) -> Config:
    parsed_config = dict(config)
    if file_path is None:
        return parsed_config

    with Path(file_path).open("r", encoding="utf-8") as config_file:
        for line in config_file:
            _merge_config_line(parsed_config, line)

    return parsed_config

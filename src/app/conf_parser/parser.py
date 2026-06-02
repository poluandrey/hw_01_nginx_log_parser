from dataclasses import dataclass
from pathlib import Path

from app.config import config


@dataclass
class Config:
    report_size: int = config["REPORT_SIZE"]
    report_dir: str | Path = config["REPORT_DIR"]
    log_dir: str | Path = config["LOG_DIR"]


def _parse_config_line(line: str) -> tuple[str, str] | None:
    stripped_line = line.strip()
    if not stripped_line or stripped_line.startswith("#") or "=" not in stripped_line:
        return None

    key, raw_setting = stripped_line.split("=", 1)
    return key.strip(), raw_setting.strip()


def _update_config(parsed_config: Config, config_key: str, raw_setting: str) -> None:
    if not raw_setting:
        return

    if config_key == "REPORT_SIZE":
        parsed_config.report_size = int(raw_setting)
    elif config_key == "REPORT_DIR":
        parsed_config.report_dir = raw_setting
    elif config_key == "LOG_DIR":
        parsed_config.log_dir = raw_setting


def _update_config_from_line(parsed_config: Config, line: str) -> None:
    parsed_line = _parse_config_line(line)
    if parsed_line is None:
        return

    config_key, raw_setting = parsed_line
    _update_config(parsed_config, config_key, raw_setting)


def parse_config(file_path: str | Path) -> Config:
    parsed_config = Config()
    with Path(file_path).open("r", encoding="utf-8") as config_file:
        for line in config_file:
            _update_config_from_line(parsed_config, line)

    return parsed_config

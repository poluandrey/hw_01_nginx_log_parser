from pathlib import Path

import pytest

from app.conf_parser.parser import Config, parse_config
from app.config import config as default_config
from app.main import PROJECT_DESCRIPTION, main, parse_args

TEST_ENCODING = "utf-8"
REPORT_SIZE = 42


def test_parse_args_returns_existing_config_path(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding=TEST_ENCODING)

    parsed_args = parse_args(["--config", str(config_file)])

    assert parsed_args.config == config_file


def test_parse_args_exits_on_missing_config() -> None:
    with pytest.raises(SystemExit):
        parse_args(["--config", "missing.yml"])


def test_main_returns_zero_for_existing_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding=TEST_ENCODING)

    exit_code = main(["--config", str(config_file)])

    assert exit_code == 0


def test_parser_description_mentions_project_goal() -> None:
    assert "Анализатор логов nginx" in PROJECT_DESCRIPTION


def test_parser_reads_config_values(tmp_path: Path) -> None:
    config_file = tmp_path / "config.txt"
    config_file.write_text(
        "# comment\nREPORT_SIZE = 42\nREPORT_DIR = ./reports\nLOG_DIR = ./logs\n",
        encoding=TEST_ENCODING,
    )

    parsed_config = parse_config(config_file)

    assert parsed_config == Config(
        report_size=REPORT_SIZE,
        report_dir="./reports",
        log_dir="./logs",
    )


def test_parser_uses_defaults_for_missing_values(tmp_path: Path) -> None:
    config_file = tmp_path / "config.txt"
    config_file.write_text("REPORT_DIR = ./custom_reports\n", encoding=TEST_ENCODING)

    parsed_config = parse_config(config_file)

    assert parsed_config.report_size == default_config["REPORT_SIZE"]
    assert parsed_config.report_dir == "./custom_reports"
    assert parsed_config.log_dir == default_config["LOG_DIR"]

import json
from pathlib import Path

import pytest

from app.main import PROJECT_DESCRIPTION, main, parse_args

TEST_ENCODING = "utf-8"
CONFIG_OPTION = "--config"
CONFIG_FILE_NAME = "config.txt"


def test_parse_args_returns_existing_config_path(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding=TEST_ENCODING)

    parsed_args = parse_args([CONFIG_OPTION, str(config_file)])

    assert parsed_args.config == config_file


def test_parse_args_exits_on_missing_config() -> None:
    with pytest.raises(SystemExit):
        parse_args([CONFIG_OPTION, "missing.yml"])


def test_main_returns_zero_for_existing_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding=TEST_ENCODING)

    exit_code = main([CONFIG_OPTION, str(config_file)])

    assert exit_code == 0


def test_parser_description_mentions_project_goal() -> None:
    assert "Анализатор логов nginx" in PROJECT_DESCRIPTION


def test_main_logs_json_to_stdout(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text("REPORT_DIR = ./custom_reports\n", encoding=TEST_ENCODING)

    exit_code = main([CONFIG_OPTION, str(config_file)])

    stdout = capsys.readouterr().out.strip()
    log_record = json.loads(stdout)
    assert exit_code == 0
    assert log_record["event"] == "config_loaded"
    assert log_record["level"] == "info"


def test_main_logs_json_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(f"LOG_FILE = {log_file}\n", encoding=TEST_ENCODING)

    exit_code = main([CONFIG_OPTION, str(config_file)])

    log_record = json.loads(log_file.read_text(encoding=TEST_ENCODING).strip())
    assert exit_code == 0
    assert log_record["event"] == "config_loaded"
    assert log_record["level"] == "info"

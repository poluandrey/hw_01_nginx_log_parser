import json
from pathlib import Path

import pytest

from app.main import main

TEST_ENCODING = "utf-8"
CONFIG_OPTION = "--config"
CONFIG_FILE_NAME = "config.txt"


def _raise_keyboard_interrupt(_args: list[str] | None = None) -> None:
    raise KeyboardInterrupt


def _read_log_records(log_output: str) -> list[dict[str, str]]:
    return [json.loads(log_line) for log_line in log_output.splitlines()]


def test_main_returns_one_for_keyboard_interrupt(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("app.main._run_with_config", _raise_keyboard_interrupt)

    exit_code = main([])

    log_record = json.loads(capsys.readouterr().out.strip())
    assert exit_code == 1
    assert log_record["event"] == "unexpected_error"
    assert log_record["level"] == "error"


def test_main_returns_zero_for_existing_config(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text("version: 1\n", encoding=TEST_ENCODING)

    exit_code = main([CONFIG_OPTION, str(config_file)])

    assert exit_code == 0


def test_main_logs_json_to_stdout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text("REPORT_DIR = ./custom_reports\n", encoding=TEST_ENCODING)

    exit_code = main([CONFIG_OPTION, str(config_file)])

    log_records = _read_log_records(capsys.readouterr().out.strip())
    assert exit_code == 0
    assert [record["event"] for record in log_records] == ["config_loaded", "no_log_found"]


def test_main_logs_json_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(f"LOG_FILE = {log_file}\n", encoding=TEST_ENCODING)

    exit_code = main([CONFIG_OPTION, str(config_file)])

    log_records = _read_log_records(
        log_file.read_text(encoding=TEST_ENCODING).strip(),
    )
    assert exit_code == 0
    assert [record["event"] for record in log_records] == ["config_loaded", "no_log_found"]

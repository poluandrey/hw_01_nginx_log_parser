import json
from pathlib import Path

import pytest

from app.main import main

TEST_ENCODING = "utf-8"
CONFIG_OPTION = "--config"
CONFIG_FILE_NAME = "config.txt"


def _read_log_records(log_output: str) -> list[dict[str, str]]:
    return [json.loads(log_line) for log_line in log_output.splitlines()]


def _build_config_text(report_dir: Path, log_dir: Path, log_file: Path | None = None) -> str:
    config_lines = [
        f"REPORT_DIR = {report_dir}",
        f"LOG_DIR = {log_dir}",
    ]
    if log_file is not None:
        config_lines.insert(0, f"LOG_FILE = {log_file}")
    config_lines.append("")
    return "\n".join(config_lines)


def test_main_logs_json_to_stdout(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(
        _build_config_text(tmp_path / "custom_reports", tmp_path / "missing_log"),
        encoding=TEST_ENCODING,
    )

    exit_code = main([CONFIG_OPTION, str(config_file)])

    log_records = _read_log_records(capsys.readouterr().out.strip())
    assert exit_code == 0
    assert log_records[0]["config_path"] is not None
    assert [record["event"] for record in log_records] == ["config_loaded", "no_log_found"]


def test_main_logs_json_to_file(tmp_path: Path) -> None:
    log_file = tmp_path / "app.log"
    config_file = tmp_path / CONFIG_FILE_NAME
    config_file.write_text(
        _build_config_text(tmp_path / "custom_reports", tmp_path / "missing_log", log_file),
        encoding=TEST_ENCODING,
    )

    exit_code = main([CONFIG_OPTION, str(config_file)])

    log_records = _read_log_records(log_file.read_text(encoding=TEST_ENCODING).strip())
    assert exit_code == 0
    assert [record["event"] for record in log_records] == ["config_loaded", "no_log_found"]


def test_main_logs_null_config_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main([])

    log_records = _read_log_records(capsys.readouterr().out.strip())
    assert exit_code == 0
    assert log_records[0]["config_path"] is None

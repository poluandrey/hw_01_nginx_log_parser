import json
from pathlib import Path

import pytest

from app.main import main

TEST_ENCODING = "utf-8"
CONFIG_OPTION = "--config"


def _raise_keyboard_interrupt(_args: list[str] | None = None) -> None:
    raise KeyboardInterrupt


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
    reports_dir = tmp_path / "custom_reports"
    config_file.write_text(
        _build_config_text(reports_dir, tmp_path / "missing_log"),
        encoding=TEST_ENCODING,
    )
    exit_code = main([CONFIG_OPTION, str(config_file)])

    assert exit_code == 0


def test_main_uses_module_config_defaults(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main([])

    assert exit_code == 0

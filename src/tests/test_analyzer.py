import json
from pathlib import Path
from typing import Any

from app.analyzer import analyze
from app.logger import configure_logger

TEST_ENCODING = "utf-8"


def _write_log_file(log_path: Path, log_content: str) -> None:
    log_path.write_text(log_content, encoding=TEST_ENCODING)


def _prepare_log_dirs(tmp_path: Path) -> tuple[Path, Path, Path]:
    log_dir = tmp_path / "logs"
    report_dir = tmp_path / "reports"
    log_file = tmp_path / "app.log"
    log_dir.mkdir()
    return log_dir, report_dir, log_file


def _build_config(log_dir: Path, report_dir: Path) -> dict[str, Any]:
    return {
        "LOG_DIR": str(log_dir),
        "REPORT_DIR": str(report_dir),
        "REPORT_SIZE": 10,
    }


def _assert_report_artifacts(report_dir: Path, log_file: Path) -> None:
    report_path = report_dir / "report-2017.06.30.html"
    assert report_path.exists()
    assert (report_dir / "jquery.tablesorter.min.js").exists()
    assert "/slow" in report_path.read_text(encoding=TEST_ENCODING)
    logged_event = json.loads(log_file.read_text(encoding=TEST_ENCODING).strip())
    assert logged_event["event"] == "report_created"


def test_analyze_creates_report_for_latest_log(tmp_path: Path) -> None:
    log_dir, report_dir, log_file = _prepare_log_dirs(tmp_path)
    _write_log_file(
        log_dir / "nginx-access-ui.log-20170629",
        '1.1.1.1 - - [29/Jun/2017:03:50:22 +0300] "GET /old HTTP/1.1" 200 100 "-" "agent" "-" "-" "-" 0.100\n',
    )
    _write_log_file(
        log_dir / "nginx-access-ui.log-20170630",
        '1.1.1.1 - - [29/Jun/2017:03:50:22 +0300] "GET /slow HTTP/1.1" 200 100 "-" "agent" "-" "-" "-" 1.000\n'
        '1.1.1.1 - - [29/Jun/2017:03:50:22 +0300] "GET /fast HTTP/1.1" 200 100 "-" "agent" "-" "-" "-" 0.100\n',
    )

    analyze(_build_config(log_dir, report_dir), configure_logger(log_file))
    _assert_report_artifacts(report_dir, log_file)

from typing import Any

from app.logs import find_latest_log, iter_log_records
from app.report import build_report_rows
from app.report_renderer import build_report_path, render_report, write_report

Config = dict[str, Any]


def analyze(config: Config, logger: Any) -> None:
    latest_log = find_latest_log(config["LOG_DIR"])
    if latest_log is None:
        logger.info("no_log_found", log_dir=config["LOG_DIR"])
        return

    report_path = build_report_path(
        report_dir=config["REPORT_DIR"],
        log_date=latest_log.log_date,
    )
    if report_path.exists():
        logger.info("report_already_exists", report_path=str(report_path))
        return

    report_rows = build_report_rows(
        log_records=iter_log_records(latest_log),
        report_size=config["REPORT_SIZE"],
    )
    write_report(report_path, render_report(report_rows))
    logger.info(
        "report_created",
        report_path=str(report_path),
        source_log=str(latest_log.path),
        records=len(report_rows),
    )

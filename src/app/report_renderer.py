import json
import shutil
from datetime import datetime
from pathlib import Path
from string import Template

from app.report import ReportRow

REPORT_TEMPLATE_PATH = Path(__file__).resolve().parent / "templates" / "report.html"
TABLESORTER_ASSET_PATH = Path(__file__).resolve().parent / "templates" / "jquery.tablesorter.min.js"


def build_report_path(report_dir: str | Path, log_date: datetime) -> Path:
    return Path(report_dir) / log_date.strftime("report-%Y.%m.%d.html")


def render_report(
    report_rows: list[ReportRow],
    template_path: str | Path = REPORT_TEMPLATE_PATH,
) -> str:
    template = Template(Path(template_path).read_text(encoding="utf-8"))
    return template.safe_substitute(
        table_json=json.dumps(report_rows, ensure_ascii=False),
    )


def write_report(report_path: str | Path, report_content: str) -> None:
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report_content, encoding="utf-8")
    shutil.copy2(TABLESORTER_ASSET_PATH, path.parent / TABLESORTER_ASSET_PATH.name)

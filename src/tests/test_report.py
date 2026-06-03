from pathlib import Path

import pytest

from app.report import build_report_rows
from app.report_renderer import render_report

EXPECTED_AVG = 0.2
EXPECTED_MEDIAN = 0.2
EXPECTED_COUNT_PERC = 66.667


def test_build_report_rows_calculates_statistics() -> None:
    report_rows = build_report_rows(
        log_records=[
            ("/api/test", 0.1),
            ("/api/test", 0.3),
            ("/api/slow", 1.0),
        ],
        report_size=10,
    )
    first_row = report_rows[0]
    second_row = report_rows[1]

    assert first_row["url"] == "/api/slow"
    assert first_row["time_sum"] == pytest.approx(1.0)
    assert second_row["url"] == "/api/test"
    assert (
        second_row["count"],
        second_row["time_avg"],
        second_row["time_med"],
        second_row["count_perc"],
    ) == pytest.approx((2, EXPECTED_AVG, EXPECTED_MEDIAN, EXPECTED_COUNT_PERC))


def test_render_report_includes_table_json(tmp_path: Path) -> None:
    template_path = tmp_path / "report.html"
    template_path.write_text("<html>$table_json</html>", encoding="utf-8")

    rendered_report = render_report(
        report_rows=[{"url": "/health", "count": 1}],
        template_path=template_path,
    )

    assert '"/health"' in rendered_report
    assert "<html>" in rendered_report

import gzip
from pathlib import Path

from app.logs import find_latest_log, iter_log_records, parse_log_line

TEST_ENCODING = "utf-8"


def test_find_latest_log_returns_latest_file(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("skip me", encoding=TEST_ENCODING)
    (tmp_path / "nginx-access-ui.log-20170629").write_text("old", encoding=TEST_ENCODING)
    (tmp_path / "nginx-access-ui.log-20170630.bz2").write_text("wrong", encoding=TEST_ENCODING)
    latest_log = tmp_path / "nginx-access-ui.log-20170701.gz"
    with gzip.open(latest_log, "wt", encoding=TEST_ENCODING) as log_file:
        log_file.write("content\n")

    found_log = find_latest_log(tmp_path)

    assert found_log is not None
    assert found_log.path == latest_log
    assert found_log.extension == ".gz"


def test_parse_log_line_extracts_url_and_time() -> None:
    log_line = (
        '1.196.116.32 - - [29/Jun/2017:03:50:22 +0300] '
        '"GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" '
        '"agent" "-" "request-id" "user-id" 0.390'
    )

    parsed_line = parse_log_line(log_line)

    assert parsed_line == ("/api/v2/banner/25019354", 0.39)


def test_iter_log_records_skips_invalid_lines(tmp_path: Path) -> None:
    log_path = tmp_path / "nginx-access-ui.log-20170630"
    log_path.write_text(
        "\n".join(
            (
                '1.1.1.1 - - [29/Jun/2017:03:50:22 +0300] "GET /ok HTTP/1.1" 200 100 "-" "agent" "-" "-" "-" 0.100',
                "broken line",
            ),
        ),
        encoding=TEST_ENCODING,
    )

    log_info = find_latest_log(tmp_path)
    if log_info:
        records = list(iter_log_records(log_info))

    assert records == [("/ok", 0.1)]

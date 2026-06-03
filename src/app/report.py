from collections import defaultdict
from statistics import median
from typing import Any, Iterable

ReportRow = dict[str, Any]
CollectedTimings = tuple[dict[str, list[float]], int, float]


def _round_metric(metric: float) -> float:
    return round(metric, 3)


def _collect_timings(
    log_records: Iterable[tuple[str, float]],
) -> CollectedTimings:
    timings_by_url: dict[str, list[float]] = defaultdict(list)
    total_count: int = 0
    total_time: float = 0
    for url, request_time in log_records:
        timings_by_url[url].append(request_time)
        total_count += 1
        total_time += request_time
    return timings_by_url, total_count, total_time


def _build_report_row(
    url: str,
    timings: list[float],
    total_count: int,
    total_time: float,
) -> ReportRow:
    count = len(timings)
    time_sum = sum(timings)
    return {
        "url": url,
        "count": count,
        "count_perc": _round_metric(count * 100 / total_count),
        "time_sum": _round_metric(time_sum),
        "time_perc": _round_metric(time_sum * 100 / total_time),
        "time_avg": _round_metric(time_sum / count),
        "time_max": _round_metric(max(timings)),
        "time_med": _round_metric(median(timings)),
    }


def build_report_rows(
    log_records: Iterable[tuple[str, float]],
    report_size: int,
) -> list[ReportRow]:
    timings_by_url, total_count, total_time = _collect_timings(log_records)
    return sorted(
        (
            _build_report_row(url, timings, total_count, total_time)
            for url, timings in timings_by_url.items()
        ),
        key=lambda row: row["time_sum"],
        reverse=True,
    )[:report_size]

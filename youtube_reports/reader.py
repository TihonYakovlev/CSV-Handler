import csv
from pathlib import Path
from typing import Iterable

from youtube_reports.models import VideoMetrics


REQUIRED_COLUMNS = frozenset(
    {
        "title",
        "ctr",
        "retention_rate",
        "views",
        "likes",
        "avg_watch_time",
    }
)


def read_video_metrics(file_paths: Iterable[str]) -> list[VideoMetrics]:
    videos: list[VideoMetrics] = []

    for file_path in file_paths:
        path = Path(file_path)
        with path.open(encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            _validate_columns(reader.fieldnames, path)

            for row in reader:
                videos.append(_parse_video(row))

    return videos


def _validate_columns(fieldnames: list[str] | None, path: Path) -> None:
    if fieldnames is None:
        raise ValueError(f"{path}: CSV file has no header")

    missing_columns = REQUIRED_COLUMNS.difference(fieldnames)
    if missing_columns:
        columns = ", ".join(sorted(missing_columns))
        raise ValueError(f"{path}: missing required columns: {columns}")


def _parse_video(row: dict[str, str]) -> VideoMetrics:
    return VideoMetrics(
        title=row["title"],
        ctr=float(row["ctr"]),
        retention_rate=float(row["retention_rate"]),
        views=int(row["views"]),
        likes=int(row["likes"]),
        avg_watch_time=float(row["avg_watch_time"]),
    )
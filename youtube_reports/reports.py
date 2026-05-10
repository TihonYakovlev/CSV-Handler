from collections.abc import Iterable, Mapping, Sequence
from typing import Protocol

from youtube_reports.models import VideoMetrics


ReportRow = Mapping[str, object]


class Report(Protocol):
    name: str
    columns: Sequence[str]

    def build(self, videos: Iterable[VideoMetrics]) -> list[ReportRow]:
        ...


class UnknownReportError(ValueError):
    pass


class ClickbaitReport:
    name = "clickbait"
    columns = ("title", "ctr", "retention_rate")

    def build(self, videos: Iterable[VideoMetrics]) -> list[ReportRow]:
        clickbait_videos = (
            video
            for video in videos
            if video.ctr > 15 and video.retention_rate < 40
        )
        sorted_videos = sorted(
            clickbait_videos,
            key=lambda video: video.ctr,
            reverse=True,
        )

        return [
            {
                "title": video.title,
                "ctr": video.ctr,
                "retention_rate": video.retention_rate,
            }
            for video in sorted_videos
        ]


REPORTS: dict[str, Report] = {
    ClickbaitReport.name: ClickbaitReport(),
}


def available_reports() -> list[str]:
    return sorted(REPORTS)


def get_report(name: str) -> Report:
    try:
        return REPORTS[name]
    except KeyError as error:
        available = ", ".join(available_reports())
        raise UnknownReportError(
            f"unknown report '{name}'. Available reports: {available}"
        ) from error
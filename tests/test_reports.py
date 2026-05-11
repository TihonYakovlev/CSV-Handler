import pytest

from youtube_reports.models import VideoMetrics
from youtube_reports.reports import ClickbaitReport, UnknownReportError, get_report


def make_video(title: str, ctr: float, retention_rate: float) -> VideoMetrics:
    return VideoMetrics(
        title=title,
        ctr=ctr,
        retention_rate=retention_rate,
        views=100,
        likes=10,
        avg_watch_time=4.5,
    )


def test_clickbait_report_filters_by_strict_ctr_and_retention_rules():
    videos = [
        make_video("matches", 16, 39),
        make_video("ctr boundary is excluded", 15, 20),
        make_video("retention boundary is excluded", 20, 40),
        make_video("low ctr is excluded", 10, 30),
        make_video("high retention is excluded", 22, 70),
    ]

    rows = ClickbaitReport().build(videos)

    assert rows == [
        {
            "title": "matches",
            "ctr": 16,
            "retention_rate": 39,
        }
    ]


def test_clickbait_report_sorts_rows_by_ctr_descending():
    videos = [
        make_video("second", 17.5, 35),
        make_video("first", 25.0, 22),
        make_video("third", 16.0, 30),
    ]

    rows = ClickbaitReport().build(videos)

    assert [row["title"] for row in rows] == ["first", "second", "third"]


def test_get_report_returns_registered_clickbait_report():
    report = get_report("clickbait")

    assert isinstance(report, ClickbaitReport)
    assert report.columns == ("title", "ctr", "retention_rate")


def test_get_report_raises_readable_error_for_unknown_report():
    with pytest.raises(UnknownReportError) as error:
        get_report("engagement")

    assert "unknown report 'engagement'" in str(error.value)
    assert "clickbait" in str(error.value)

import pytest

from youtube_reports.models import VideoMetrics
from youtube_reports.reader import read_video_metrics


def test_read_video_metrics_combines_multiple_files(tmp_path):
    first_file = tmp_path / "first.csv"
    second_file = tmp_path / "second.csv"

    first_file.write_text(
        "\n".join(
            [
                "title,ctr,retention_rate,views,likes,avg_watch_time",
                "First video,18.2,35,45200,1240,4.2",
            ]
        ),
        encoding="utf-8",
    )
    second_file.write_text(
        "\n".join(
            [
                "title,ctr,retention_rate,views,likes,avg_watch_time",
                "Second video,9.5,82,31500,890,8.9",
            ]
        ),
        encoding="utf-8",
    )

    videos = read_video_metrics([str(first_file), str(second_file)])

    assert videos == [
        VideoMetrics(
            title="First video",
            ctr=18.2,
            retention_rate=35,
            views=45200,
            likes=1240,
            avg_watch_time=4.2,
        ),
        VideoMetrics(
            title="Second video",
            ctr=9.5,
            retention_rate=82,
            views=31500,
            likes=890,
            avg_watch_time=8.9,
        ),
    ]


def test_read_video_metrics_reports_missing_required_columns(tmp_path):
    csv_file = tmp_path / "broken.csv"
    csv_file.write_text(
        "\n".join(
            [
                "title,ctr",
                "First video,18.2",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as error:
        read_video_metrics([str(csv_file)])

    assert "missing required columns" in str(error.value)
    assert "retention_rate" in str(error.value)

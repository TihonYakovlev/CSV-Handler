from youtube_reports.reader import read_video_metrics
from youtube_reports.reports import get_report


def main() -> int:
    videos = read_video_metrics(["stats1.csv", "stats2.csv"])
    report = get_report("clickbait")
    rows = report.build(videos)

    for row in rows:
        print(row)

    return 0
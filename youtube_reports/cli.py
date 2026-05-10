from youtube_reports.reader import read_video_metrics
from youtube_reports.render import render_table
from youtube_reports.reports import get_report


def main() -> int:
    videos = read_video_metrics(["stats1.csv", "stats2.csv"])
    report = get_report("clickbait")
    rows = report.build(videos)

    print(render_table(rows, report.columns))
    return 0

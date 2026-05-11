import argparse
from collections.abc import Sequence

from youtube_reports.reader import read_video_metrics
from youtube_reports.render import render_table
from youtube_reports.reports import available_reports, get_report


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        videos = read_video_metrics(args.files)
        report = get_report(args.report)
        rows = report.build(videos)
    except FileNotFoundError as error:
        parser.error(f"file not found: {error.filename}")
    except ValueError as error:
        parser.error(str(error))

    print(render_table(rows, report.columns))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build reports from YouTube video metrics CSV files.",
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="paths to CSV files with video metrics",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=available_reports(),
        help="report name",
    )
    return parser
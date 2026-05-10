from youtube_reports.reader import read_video_metrics


def main() -> int:
    videos = read_video_metrics(["stats1.csv"])
    print(videos[0])
    print(videos[1])
    print(f"Total videos: {len(videos)}")
    return 0
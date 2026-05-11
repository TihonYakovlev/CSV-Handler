import pytest

from youtube_reports.cli import main


def test_cli_prints_clickbait_report_from_multiple_example_files(capsys):
    exit_code = main(
        [
            "--files",
            "stats1.csv",
            "stats2.csv",
            "--report",
            "clickbait",
        ]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "title" in captured.out
    assert "ctr" in captured.out
    assert "retention_rate" in captured.out
    assert "Секрет который скрывают тимлиды" in captured.out
    assert "Почему продакшн упал в пятницу вечером" in captured.out
    assert "Почему сеньоры не носят галстуки" not in captured.out
    assert "views" not in captured.out


def test_cli_sorts_report_by_ctr_descending(capsys):
    main(
        [
            "--files",
            "stats1.csv",
            "stats2.csv",
            "--report",
            "clickbait",
        ]
    )

    output = capsys.readouterr().out

    assert output.index("Секрет который скрывают тимлиды") < output.index(
        "Почему продакшн упал в пятницу вечером"
    )
    assert output.index("Почему продакшн упал в пятницу вечером") < output.index(
        "Как я неделю не мыл кружку и выгорел"
    )


def test_cli_exits_with_error_for_missing_file(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--files", "none.csv", "--report", "clickbait"])

    captured = capsys.readouterr()

    assert error.value.code == 2
    assert "file not found" in captured.err


def test_cli_exits_with_error_for_unknown_report(capsys):
    with pytest.raises(SystemExit) as error:
        main(["--files", "stats1.csv", "--report", "unknown"])

    captured = capsys.readouterr()

    assert error.value.code == 2
    assert "invalid choice" in captured.err

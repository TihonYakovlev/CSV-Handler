from youtube_reports.render import render_table


def test_render_table_uses_only_requested_columns():
    table = render_table(
        [
            {
                "title": "First video",
                "ctr": 25.0,
                "retention_rate": 22,
                "views": 1000,
            }
        ],
        ["title", "ctr", "retention_rate"],
    )

    assert "title" in table
    assert "ctr" in table
    assert "retention_rate" in table
    assert "First video" in table
    assert "25" in table
    assert "22" in table
    assert "views" not in table
    assert "1000" not in table

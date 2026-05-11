from collections.abc import Mapping, Sequence
from tabulate import tabulate


def render_table(rows: Sequence[Mapping[str, object]], columns: Sequence[str]) -> str:
    data = [[row.get(col, "") for col in columns] for row in rows]

    return tabulate(
        data,
        headers=columns,
        tablefmt="grid",
        floatfmt="g",
        missingval="",
    )

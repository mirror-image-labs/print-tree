from __future__ import annotations
from typing import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from print_tree.matcher import Matcher


def iter_files(
    root: Path,
    matcher: "Matcher",
) -> Iterable[Path]:

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if matcher.is_included(path):
            yield path

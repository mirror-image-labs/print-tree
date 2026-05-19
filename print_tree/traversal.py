from __future__ import annotations
from typing import Iterable
from pathlib import Path
from typing import TYPE_CHECKING
from os.path import commonpath


if TYPE_CHECKING:
    from print_tree.matcher import Matcher


def iter_files(
    root: Path,
    matcher: "Matcher",
) -> Iterable[Path]:
    """Recursively iterate over files in a directory, yielding only
    those that match the provided matcher."""
    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if matcher.is_included(path):
            yield path


def common_ancestor(files: list[Path]) -> str:
    """Find the common ancestor directory for a list of file paths."""
    if not files:
        return "."

    if len(files) == 1:
        return str(files[0].parent)

    common_path = Path(files[0])

    for path in files[1:]:
        common_path = Path(commonpath([str(common_path), str(path)]))

    return str(common_path)

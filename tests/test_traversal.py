# tests/test_traversal.py

from pathlib import Path

from print_tree.matcher import Matcher
from print_tree.traversal import iter_files


def test_iter_files(tmp_path: Path):

    (tmp_path / "src").mkdir()

    (tmp_path / "src" / "main.py").write_text(
        "print('hello')"
    )

    (tmp_path / "README.md").write_text(
        "# Hello"
    )

    matcher = Matcher(
        root=tmp_path,
        include_patterns=["**/*.py"],
        ignore_patterns=[],
    )

    files = list(iter_files(tmp_path, matcher))

    assert len(files) == 1

    assert files[0].name == "main.py"

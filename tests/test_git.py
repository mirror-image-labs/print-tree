# tests/test_git.py

from pathlib import Path

from print_tree.git import is_git_repo


def test_non_git_repo(tmp_path: Path):
    assert not is_git_repo(tmp_path)

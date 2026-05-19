# tests/test_matcher.py

from pathlib import Path

from print_tree.matcher import Matcher


def test_ignore_patterns():

    matcher = Matcher(
        root=Path("/tmp/project"),
        include_patterns=[],
        ignore_patterns=[
            "**/node_modules/**",
            "**/*.lock",
        ],
    )

    assert not matcher.is_included(
        Path("/tmp/project/node_modules/foo.js")
    )

    assert not matcher.is_included(
        Path("/tmp/project/uv.lock")
    )

    assert matcher.is_included(
        Path("/tmp/project/src/main.py")
    )


def test_include_patterns():

    matcher = Matcher(
        root=Path("/tmp/project"),
        include_patterns=[
            "**/*.py",
        ],
        ignore_patterns=[],
    )

    assert matcher.is_included(
        Path("/tmp/project/src/main.py")
    )

    assert not matcher.is_included(
        Path("/tmp/project/src/main.ts")
    )


def test_include_and_ignore_patterns():

    matcher = Matcher(
        root=Path("/tmp/project"),
        include_patterns=[
            "**/*.py",
        ],
        ignore_patterns=[
            "**/node_modules/**",
        ],
    )

    assert matcher.is_included(
        Path("/tmp/project/src/main.py")
    )

    # current semantics:
    # includes override ignores

    assert matcher.is_included(
        Path("/tmp/project/node_modules/foo.py")
    )


def test_relative_path():

    matcher = Matcher(
        root=Path("/tmp/project"),
        include_patterns=[],
        ignore_patterns=[],
    )

    path = Path("/tmp/project/src/main.py")

    assert matcher.relative_path(path) == "src/main.py"

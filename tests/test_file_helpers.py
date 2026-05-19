# tests/test_file_helpers.py

from pathlib import Path

from print_tree.file_helpers import (
    is_probably_text_file,
    detect_lexer,
)


def test_text_file_detection(tmp_path: Path):

    path = tmp_path / "hello.txt"

    path.write_text("hello")

    assert is_probably_text_file(path)


def test_binary_file_detection(tmp_path: Path):

    path = tmp_path / "data.bin"

    path.write_bytes(b"\x00\x01\x02")

    assert not is_probably_text_file(path)


def test_detect_lexer():

    assert detect_lexer(Path("main.py")) == "python"

    assert detect_lexer(Path("main.ts")) == "typescript"

    assert detect_lexer(Path("unknown.xyz")) == "text"

# tests/test_cli.py

from pathlib import Path

from typer.testing import CliRunner

from print_tree.cli import app


runner = CliRunner()


def test_cli_summary(tmp_path: Path):
    """Test that the summary option correctly counts files."""
    (tmp_path / "main.py").write_text(
        "print('hello')"
    )

    result = runner.invoke(
        app,
        [
            str(tmp_path),
            "--summary",
        ],
    )

    assert "main.py" in result.stdout
    assert "Found 1 files" in result.stdout


def test_cli_summary_multiple_files(tmp_path: Path):
    """Test that the summary option correctly counts multiple files."""
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "console.py").write_text("print('console')")
    (tmp_path / "loader.py").write_text("print('loader')")

    result = runner.invoke(
        app,
        [
            str(tmp_path),
            "--summary",
        ],
    )

    assert "main.py" in result.stdout
    assert "console.py" in result.stdout
    assert "loader.py" in result.stdout
    assert "Found 3 files" in result.stdout


def test_cli_json(tmp_path: Path):
    """Test that the JSON option correctly outputs file information."""

    (tmp_path / "main.py").write_text(
        "print('hello')"
    )

    result = runner.invoke(
        app,
        [
            str(tmp_path),
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert "file_path" in result.stdout
    assert "file_contents" in result.stdout

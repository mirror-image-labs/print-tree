from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Iterable, Optional, TypedDict

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.text import Text
from print_tree.git import load_gitignore_patterns
from print_tree.file_helpers import is_probably_text_file, read_file, detect_lexer
from print_tree.traversal import iter_files
from print_tree.matcher import Matcher


app = typer.Typer(
    add_completion=False,
    help="Recursively print file paths and contents.",
)

console = Console()

DEFAULT_IGNORES = {
    ".git/",
    ".svn/",
    ".hg/",
    "**/__pycache__/",
    "**/.DS_Store",
    "**/node_modules/",
    "**/.venv/",
    "**/dist/",
    "**/build/",
    "**/*.lock",
    ".gitignore",
    ".python-version",
    "README.md",
    "pyproject.toml",
}


class ResultType(TypedDict):
    file_path: str
    file_contents: str


@app.command()
def print_files(
    directory: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
        help="Root directory to scan.",
    ),
    include: list[str] = typer.Option(
        None,
        "--include",
        help="Glob patterns to include.",
    ),
    ignore: list[str] = typer.Option(
        None,
        "--ignore",
        help="Glob patterns to ignore.",
    ),
    encoding: str = typer.Option(
        "utf-8",
        "--encoding",
        help="File encoding.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit JSON instead of rich terminal output.",
    ),
    include_binary: bool = typer.Option(
        False,
        "--binary",
        help="Include binary files.",
    ),
    max_size_kb: int = typer.Option(
        1024,
        "--max-size-kb",
        help="Maximum file size to read.",
    ),
    no_gitignore: bool = typer.Option(
        False,
        "--no-gitignore",
        help="Disable git-aware file discovery.",
    ),
    summary: bool = typer.Option(
        False,
        "--summary",
        help="Only print file paths, not contents.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Enable verbose logging.",
    ),
    pretty: bool = typer.Option(
        False,
        "--pretty",
        help="Enable pretty output with syntax highlighting and panels.",
    ),
) -> None:
    """
    Recursively print file paths and contents.
    """

    ignore_patterns = list(DEFAULT_IGNORES)

    if not no_gitignore:
        gitignore_patterns = load_gitignore_patterns(
            directory
        )
        ignore_patterns.extend(gitignore_patterns)

    if ignore:
        ignore_patterns.extend(ignore)

    if verbose:
        console.print(f"[green]Number of ignore patterns: {len(ignore_patterns)}[/green]")
        for pattern in ignore_patterns:
            console.print(f"  [yellow]{pattern}[/yellow]")

    matcher = Matcher(
        root=directory,
        include_patterns=include or [],
        ignore_patterns=ignore_patterns,
    )

    files = list(iter_files(directory, matcher))

    results: list[ResultType] = []
    for path in files:
        result = process_path(
            path,
            max_size_kb,
            include_binary,
            encoding,
            json_output,
            directory,
            summary,
            pretty,
        )
        if result:
            results.append(result)
    if json_output:
        console.print_json(json.dumps(results))

    console.print(
        f"[bold blue]Found {len(files)} files[/bold blue]"
    )


def process_path(
    path: Path,
    max_size_kb: int,
    include_binary: bool,
    encoding: str,
    json_output: bool,
    directory: Path,
    summary: bool,
    pretty: bool,
) -> ResultType | None:
    try:
        if path.stat().st_size > max_size_kb * 1024:
            console.print(f"[yellow]Skipping large file:[/yellow] {path}")
            return

        if (
            not include_binary
            and not is_probably_text_file(path)
        ):
            console.print(f"[dim]Skipping binary file:[/dim] {path}")
            return

        content = read_file(path, encoding)

        relative_path = path.relative_to(directory)

        if json_output:
            return {
                "file_path": str(relative_path),
                "file_contents": content,
            }

        header = Text(
            str(relative_path),
            style="bold cyan",
        )

        if summary:
            console.print(header)
        else:
            if pretty:
                syntax = Syntax(
                    content,
                    lexer=detect_lexer(path),
                    theme="monokai",
                    line_numbers=True,
                    word_wrap=False,
                )

                console.print(
                    Panel(
                        syntax,
                        title=header,
                        border_style="blue",
                    )
                )
            else:
                console.print(f"[bold cyan]# {header}[/bold cyan]")
                console.print(content)

    except UnicodeDecodeError:
        console.print(f"[red]Encoding error:[/red] {path}")

    except PermissionError:
        console.print(f"[red]Permission denied:[/red] {path}")

    except Exception as e:
        console.print(f"[red]Error reading {path}:[/red] {e}")

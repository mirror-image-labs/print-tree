
from pathlib import Path
import subprocess
from rich import print


def is_git_repo(root: Path, verbose: bool = False) -> bool:
    """
    Check whether the directory is inside a git repository.
    """

    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    rv = result.returncode == 0
    if verbose:
        if rv:
            print(f"[green]Git repository detected at: {root}[/green]")
        else:
            print(f"[yellow]No git repository detected at: {root}[/yellow]")

    return rv


def load_gitignore_patterns(
    root: Path,
    verbose: bool = False,
) -> list[str]:
    """
    Load .gitignore patterns from the repository, including nested .gitignore files.
    """
    patterns: list[str] = []

    if not is_git_repo(root, verbose=verbose):
        return patterns

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return patterns

    git_root = Path(result.stdout.strip())
    for gitignore in git_root.rglob(".gitignore"):
        try:
            rel_dir = gitignore.parent.relative_to(git_root)
            with gitignore.open() as f:
                for line in f:
                    line = line.strip()

                    if not line:
                        continue

                    if line.startswith("#"):
                        continue

                    # Prefix nested .gitignore patterns
                    # so matching remains rooted correctly.
                    if str(rel_dir) != ".":

                        pattern = (
                            rel_dir.as_posix().rstrip("/")
                            + "/"
                            + line.lstrip("/")
                        )

                    else:
                        pattern = line

                    patterns.append(pattern)

        except Exception:
            continue

    return patterns

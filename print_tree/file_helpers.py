from pathlib import Path
import mimetypes


def is_probably_text_file(path: Path) -> bool:
    """
    Heuristic check for text files.
    """

    mime, _ = mimetypes.guess_type(str(path))

    if mime and mime.startswith("text/"):
        return True

    try:
        with path.open("rb") as f:
            chunk = f.read(8192)

        if b"\x00" in chunk:
            return False

        chunk.decode("utf-8")
        return True

    except Exception:
        return False


def read_file(path: Path, encoding: str) -> str:
    return path.read_text(encoding=encoding)


def detect_lexer(path: Path) -> str:
    ext = path.suffix.lower()

    mapping = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".tsx": "tsx",
        ".jsx": "jsx",
        ".json": "json",
        ".md": "markdown",
        ".sh": "bash",
        ".zsh": "bash",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".html": "html",
        ".css": "css",
        ".toml": "toml",
        ".rs": "rust",
        ".go": "go",
        ".java": "java",
        ".c": "c",
        ".cpp": "cpp",
    }

    return mapping.get(ext, "text")

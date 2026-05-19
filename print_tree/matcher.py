from dataclasses import dataclass
from pathlib import Path
import pathspec


@dataclass
class Matcher:
    """
    Unified include/ignore matcher using gitignore semantics.
    """

    root: Path
    include_patterns: list[str]
    ignore_patterns: list[str]

    def __post_init__(self) -> None:
        self.include_spec = (
            pathspec.PathSpec.from_lines(
                "gitignore",
                self.include_patterns,
            )
            if self.include_patterns
            else None
        )
        self.ignore_spec = pathspec.PathSpec.from_lines(
            "gitignore",
            self.ignore_patterns,
        )

    def relative_path(self, path: Path) -> str:
        """Convert an absolute path to a relative path from the root, using POSIX separators."""
        rel = path.relative_to(self.root)
        s = rel.as_posix()
        if path.is_dir():
            s += "/"
        return s

    def is_included(self, path: Path) -> bool:
        """Check if a path is included based on include and ignore patterns."""

        relative = self.relative_path(path)

        # Include patterns are authoritative.
        # If includes are specified:
        #
        #   - matching include => included
        #   - non-matching include => excluded
        #
        # Ignore patterns cannot override includes.

        if self.include_spec:

            return self.include_spec.match_file(relative)

        # No include filters:
        # apply ignore filters only.

        return not self.ignore_spec.match_file(relative)

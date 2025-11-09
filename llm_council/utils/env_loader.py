"""Helpers for loading environment variables from well-known locations."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

from dotenv import load_dotenv

_DEFAULT_FILENAMES: Sequence[str] = (".env",)


def _candidate_paths(config_path: Optional[Path]) -> Iterable[Path]:
    """Yield candidate directories that may contain environment files."""

    package_dir = Path(__file__).resolve().parents[1]
    project_root = package_dir.parent

    potential_dirs = [
        Path.cwd(),
        package_dir,
        project_root,
    ]

    if config_path is not None:
        potential_dirs.insert(0, config_path.parent)

    # User-specific configuration directories
    xdg_config = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    potential_dirs.extend(
        [
            xdg_config / "llm-council",
            Path.home() / ".llm-council",
        ]
    )

    seen: set[Path] = set()
    for directory in potential_dirs:
        try:
            resolved = directory.resolve()
        except FileNotFoundError:
            continue
        if resolved in seen:
            continue
        seen.add(resolved)
        for filename in _DEFAULT_FILENAMES:
            yield resolved / filename


def load_environment(config_path: Optional[Path | str] = None, *, override: bool = False) -> List[Path]:
    """Load environment variables from .env files.

    Args:
        config_path: Optional path to the active configuration file.
        override: Whether to override existing environment variables.

    Returns:
        A list of .env paths that were successfully loaded.
    """

    if config_path is not None:
        raw_path = Path(config_path).expanduser()
        try:
            path_obj = raw_path.resolve(strict=False)
        except FileNotFoundError:
            path_obj = raw_path
    else:
        path_obj = None
    loaded_paths: List[Path] = []

    for candidate in _candidate_paths(path_obj):
        if not candidate.exists():
            continue
        if load_dotenv(candidate, override=override):
            loaded_paths.append(candidate)

    return loaded_paths


__all__ = ["load_environment"]

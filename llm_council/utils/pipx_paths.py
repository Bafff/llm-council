from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Callable, Iterable, List, Sequence


Runner = Callable[[Sequence[str]], subprocess.CompletedProcess]


def _default_runner(args: Sequence[str]) -> subprocess.CompletedProcess:
    return subprocess.run(  # type: ignore[return-value]
        args,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def discover_pipx_bin_paths(
    env: dict[str, str] | None = None,
    runner: Runner | None = None,
) -> List[str]:
    """Return candidate directories that may contain pipx-installed binaries."""

    env_map = dict(os.environ if env is None else env)
    runner = runner or _default_runner
    candidates: list[str] = []

    for value in _collect_pipx_environment_values(runner):
        _append_unique(candidates, value)

    for key in ("PIPX_BIN_DIR",):
        value = env_map.get(key)
        if value:
            _append_unique(candidates, value)

    pipx_home = env_map.get("PIPX_HOME")
    if pipx_home:
        _append_unique(candidates, Path(pipx_home) / "bin")

    home = Path(env_map.get("HOME", "~")).expanduser()
    _append_unique(candidates, home / ".local" / "bin")

    return candidates


def _collect_pipx_environment_values(runner: Runner) -> Iterable[str]:
    try:
        result = runner(["pipx", "environment", "--value", "BIN_DIR"])
    except (FileNotFoundError, subprocess.CalledProcessError):
        return []

    stdout = (result.stdout or "").strip()
    if not stdout:
        return []

    return [stdout]


def _append_unique(collection: list[str], value: os.PathLike[str] | str) -> None:
    path = str(Path(value).expanduser())
    if path not in collection:
        collection.append(path)


__all__ = ["discover_pipx_bin_paths"]


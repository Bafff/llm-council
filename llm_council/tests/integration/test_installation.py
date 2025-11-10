"""Integration tests covering installation and console script wiring."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], *, env: dict[str, str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run a subprocess and raise a useful error message on failure."""

    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )


def test_package_install_exposes_console_script(tmp_path: Path) -> None:
    """Installing the project should expose a working ``llm-council`` CLI."""

    project_root = Path(__file__).resolve().parents[3]
    venv_dir = tmp_path / "venv"

    _run([sys.executable, "-m", "venv", str(venv_dir)], env=os.environ.copy())

    bin_dir = venv_dir / ("Scripts" if os.name == "nt" else "bin")
    python_bin = bin_dir / ("python.exe" if os.name == "nt" else "python")
    pip_bin = bin_dir / ("pip.exe" if os.name == "nt" else "pip")

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}" + env.get("PATH", "")
    env["VIRTUAL_ENV"] = str(venv_dir)
    env.pop("PYTHONPATH", None)

    _run([str(pip_bin), "install", str(project_root)], env=env)

    version_result = _run([str(bin_dir / "llm-council"), "version"], env=env, cwd=tmp_path)
    assert "LLM Council v" in version_result.stdout

    import_result = _run(
        [str(python_bin), "-c", "import llm_council; print(llm_council.__version__)"],
        env=env,
        cwd=tmp_path,
    )
    assert import_result.stdout.strip(), "llm_council should expose a version string"

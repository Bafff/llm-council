import subprocess
from types import SimpleNamespace

from llm_council.utils import pipx_paths


def make_runner(stdout: str | None = None, error: Exception | None = None):
    def _runner(cmd):
        if error is not None:
            raise error
        assert cmd == ["pipx", "environment", "--value", "BIN_DIR"]
        return SimpleNamespace(stdout=stdout)

    return _runner


def test_discovers_bin_dir_from_pipx_environment(tmp_path):
    env = {"HOME": str(tmp_path)}
    runner = make_runner(stdout="/tmp/pipx/bin\n")

    paths = pipx_paths.discover_pipx_bin_paths(env=env, runner=runner)

    assert paths[0] == "/tmp/pipx/bin"
    # The fallback to ~/.local/bin should also be present.
    assert str(tmp_path / ".local" / "bin") in paths


def test_discovers_bin_dir_from_env_fallbacks(tmp_path):
    env = {
        "HOME": str(tmp_path),
        "PIPX_BIN_DIR": "/custom/bin",
        "PIPX_HOME": "/pipx-home",
    }
    runner = make_runner(error=FileNotFoundError())

    paths = pipx_paths.discover_pipx_bin_paths(env=env, runner=runner)

    assert paths[:2] == ["/custom/bin", "/pipx-home/bin"]
    assert str(tmp_path / ".local" / "bin") == paths[-1]


def test_filters_duplicate_paths(tmp_path):
    home = str(tmp_path)
    env = {"HOME": home, "PIPX_BIN_DIR": str(tmp_path / ".local" / "bin")}
    runner = make_runner(stdout=str(tmp_path / ".local" / "bin"))

    paths = pipx_paths.discover_pipx_bin_paths(env=env, runner=runner)

    assert paths == [str(tmp_path / ".local" / "bin")]


def test_handles_non_zero_exit(tmp_path):
    env = {"HOME": str(tmp_path)}

    def runner(_cmd):
        raise subprocess.CalledProcessError(returncode=1, cmd=["pipx", "environment"])

    paths = pipx_paths.discover_pipx_bin_paths(env=env, runner=runner)

    assert paths == [str(tmp_path / ".local" / "bin")]


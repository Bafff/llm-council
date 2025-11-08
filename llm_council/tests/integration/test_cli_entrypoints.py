"""Integration tests covering the published CLI entry points."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CLI_MODULE = [sys.executable, "-m", "llm_council.cli"]


def _base_env() -> dict:
    """Return a clean environment for invoking the CLI."""

    env = os.environ.copy()

    # Remove any pre-existing API credentials to control the auth path taken by adapters.
    for key in [
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
        "OPENROUTER_API_KEY",
    ]:
        env.pop(key, None)

    # Ensure the current checkout is importable when running via ``python -m``.
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    return env


@pytest.mark.integration
def test_cli_models_with_api_key(tmp_path):
    """Running the CLI with API keys should authenticate adapters via the key path."""

    env = _base_env()
    env["OPENROUTER_API_KEY"] = "sk-or-example"

    result = subprocess.run(
        [*CLI_MODULE, "models"],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "GPT-4 Turbo" in result.stdout
    assert "Authenticated via API key" in result.stdout


@pytest.mark.integration
def test_cli_models_with_cli_credentials(tmp_path):
    """CLI-discovered credentials should be used when API keys are absent."""

    env = _base_env()

    fake_home = tmp_path / "home"
    openai_config = fake_home / ".config" / "openai" / "config.json"
    openai_config.parent.mkdir(parents=True)
    openai_config.write_text(json.dumps({"api_key": "cli-session-key"}))

    env["HOME"] = str(fake_home)

    result = subprocess.run(
        [*CLI_MODULE, "models"],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "GPT-4 Turbo" in result.stdout
    assert "Authenticated via OpenAI CLI" in result.stdout

"""Integration tests covering the published CLI entry points."""

import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CLI_MODULE = [sys.executable, "-m", "llm_council.cli"]


def _pythonpath_env() -> dict:
    """Return the current environment with PYTHONPATH configured for local imports."""

    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    return env


def _write_single_adapter_config(path: Path, *, use_cli_auth: bool) -> None:
    """Persist a minimal config that enables only the OpenRouter adapter."""

    path.write_text(
        dedent(
            f"""
            models:
              gpt4:
                enabled: true
                adapter: openrouter
                model_id: "openai/gpt-4-turbo"
                display_name: "GPT-4 Turbo"
                weight: 1.0
                use_cli_auth: {str(use_cli_auth).lower()}

            auth:
              cli_sessions:
                enabled: true
              env_vars:
                openrouter_api_key: OPENROUTER_API_KEY
                openai_api_key: OPENAI_API_KEY

            output:
              show_individual_responses: false
              show_confidence_scores: false
              show_synthesis_reasoning: false
            """
        ).strip()
    )


@pytest.mark.integration
def test_cli_models_with_api_key(tmp_path):
    """Running the CLI with real API keys should exercise the API-key auth path."""

    env = _pythonpath_env()
    api_keys = [
        env.get("OPENROUTER_API_KEY"),
        env.get("OPENAI_API_KEY"),
    ]

    if not any(api_keys):
        pytest.skip("Set OPENROUTER_API_KEY or OPENAI_API_KEY to run live API-key tests")

    config_path = tmp_path / "config.yaml"
    _write_single_adapter_config(config_path, use_cli_auth=False)

    result = subprocess.run(
        [*CLI_MODULE, "models", "--config", str(config_path)],
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

    cli_config = os.environ.get("LLM_COUNCIL_OPENAI_CLI_CONFIG")
    if not cli_config or not Path(cli_config).exists():
        pytest.skip("Set LLM_COUNCIL_OPENAI_CLI_CONFIG to a real OpenAI CLI config.json to test CLI auth")

    env = _pythonpath_env()
    for key in [
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
        "OPENROUTER_API_KEY",
    ]:
        env.pop(key, None)

    fake_home = tmp_path / "home"
    target_config = fake_home / ".config" / "openai" / "config.json"
    target_config.parent.mkdir(parents=True)
    target_config.write_bytes(Path(cli_config).read_bytes())

    env["HOME"] = str(fake_home)

    config_path = tmp_path / "config.yaml"
    _write_single_adapter_config(config_path, use_cli_auth=True)

    result = subprocess.run(
        [*CLI_MODULE, "models", "--config", str(config_path)],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "GPT-4 Turbo" in result.stdout
    assert "Authenticated via OpenAI CLI" in result.stdout or "Authenticated via ChatGPT CLI" in result.stdout


@pytest.mark.integration
def test_cli_ask_sample_request(tmp_path):
    """Run a live sample request using the ask command to ensure end-to-end execution."""

    env = _pythonpath_env()
    api_keys = [
        env.get("OPENROUTER_API_KEY"),
        env.get("OPENAI_API_KEY"),
    ]

    if not any(api_keys):
        pytest.skip("Set OPENROUTER_API_KEY or OPENAI_API_KEY to run live sample requests")

    config_path = tmp_path / "config.yaml"
    _write_single_adapter_config(config_path, use_cli_auth=False)

    result = subprocess.run(
        [
            *CLI_MODULE,
            "ask",
            "What is 2 + 2?",
            "--hide-individual",
            "--config",
            str(config_path),
        ],
        cwd=PROJECT_ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Synthesized Answer" in result.stdout


@pytest.mark.integration
def test_cli_models_loads_env_file(tmp_path):
    """The CLI should load a local .env file when no API keys are exported."""

    env = _pythonpath_env()
    for key in [
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
        "OPENROUTER_API_KEY",
    ]:
        env.pop(key, None)

    env_file = tmp_path / ".env"
    env_file.write_text("OPENROUTER_API_KEY=dotenv-test-key\n")

    config_path = tmp_path / "config.yaml"
    _write_single_adapter_config(config_path, use_cli_auth=False)

    result = subprocess.run(
        [*CLI_MODULE, "models", "--config", str(config_path)],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Authenticated via API key" in result.stdout

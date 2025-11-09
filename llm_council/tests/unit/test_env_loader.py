"""Tests for the environment loading helpers."""

import os
from pathlib import Path

import pytest

from llm_council.utils.env_loader import load_environment


@pytest.fixture(autouse=True)
def clear_test_variables():
    """Ensure test-specific environment variables are cleared before and after each test."""
    keys = ["LLM_COUNCIL_TEST_ONE", "LLM_COUNCIL_TEST_TWO"]
    original = {key: os.environ.get(key) for key in keys}
    for key in keys:
        os.environ.pop(key, None)
    yield
    for key, value in original.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def test_load_environment_uses_current_working_directory(tmp_path, monkeypatch):
    """A .env file in the working directory should be loaded automatically."""

    monkeypatch.chdir(tmp_path)
    env_file = tmp_path / ".env"
    env_file.write_text("LLM_COUNCIL_TEST_ONE=from_cwd\n")

    loaded = load_environment()

    assert env_file in loaded
    assert os.environ["LLM_COUNCIL_TEST_ONE"] == "from_cwd"


def test_load_environment_prioritizes_config_directory(tmp_path):
    """When a config path is provided, its sibling .env should be loaded."""

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "config.yaml"
    config_file.write_text("models: {}\n")

    env_file = config_dir / ".env"
    env_file.write_text("LLM_COUNCIL_TEST_TWO=config_value\n")

    loaded = load_environment(config_path=config_file)

    assert env_file in loaded
    assert os.environ["LLM_COUNCIL_TEST_TWO"] == "config_value"

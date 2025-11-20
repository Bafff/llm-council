"""Tests for adapter authentication control flow and headers."""

import asyncio
from unittest.mock import patch

from llm_council.adapters.claude_adapter import ClaudeAdapter
from llm_council.adapters.gemini_adapter import GeminiAdapter
from llm_council.adapters.openrouter_adapter import OpenRouterAdapter


class TestApiKeyFallbackWhenCliDisabled:
    """Ensure adapters fall back to API keys when CLI auth is disabled."""

    def test_claude_adapter_uses_api_key_when_cli_disabled(self):
        adapter = ClaudeAdapter({"display_name": "Claude", "use_cli_auth": False})

        with patch.object(adapter, "_authenticate_via_api_key", return_value=True) as mock_api:
            assert adapter.authenticate() is True
            mock_api.assert_called_once()

    def test_gemini_adapter_uses_api_key_when_cli_disabled(self):
        adapter = GeminiAdapter({"display_name": "Gemini", "use_cli_auth": False})

        with patch.object(adapter, "_authenticate_via_api_key", return_value=True) as mock_api:
            assert adapter.authenticate() is True
            mock_api.assert_called_once()

    def test_openrouter_adapter_uses_api_key_when_cli_disabled(self):
        adapter = OpenRouterAdapter({"display_name": "OpenRouter", "use_cli_auth": False})

        with patch.object(adapter, "_authenticate_via_api_key", return_value=True) as mock_api:
            assert adapter.authenticate() is True
            mock_api.assert_called_once()


class TestOpenRouterModelNormalization:
    """Verify OpenRouter models are normalized for OpenAI base URL."""

    def test_normalizes_vendor_prefixed_model_for_openai(self):
        adapter = OpenRouterAdapter({"display_name": "OpenRouter"})
        adapter.model_id = "openai/gpt-4-turbo"
        adapter.base_url = "https://api.openai.com/v1"

        assert adapter._normalize_model_id() == "gpt-4-turbo"

    def test_keeps_vendor_prefixed_model_for_openrouter(self):
        adapter = OpenRouterAdapter({"display_name": "OpenRouter"})
        adapter.model_id = "openai/gpt-4-turbo"
        adapter.base_url = "https://openrouter.ai/api/v1"

        assert adapter._normalize_model_id() == "openai/gpt-4-turbo"


def test_gemini_query_uses_bearer_header_for_cli_tokens(monkeypatch):
    """gcloud CLI bearer tokens must be sent via Authorization header."""

    adapter = GeminiAdapter({"display_name": "Gemini"})
    adapter.bearer_token = "gcloud-token"
    adapter.api_key = None

    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "candidates": [
                    {"content": {"parts": [{"text": "hello"}]}}
                ],
                "usageMetadata": {"totalTokenCount": 42},
            }

    captured = {}

    class DummyClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, url, headers=None, json=None):
            captured["headers"] = headers
            return DummyResponse()

    monkeypatch.setattr("httpx.AsyncClient", lambda timeout=30.0: DummyClient())

    response = asyncio.run(adapter.query("hi"))

    assert response.success is True
    assert captured["headers"].get("Authorization") == "Bearer gcloud-token"
    assert "x-goog-api-key" not in captured["headers"]

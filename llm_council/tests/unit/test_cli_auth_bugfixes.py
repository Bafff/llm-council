"""
TDD Tests for CLI Authentication Bug Fixes

Tests for:
1. Bug: Gemini adapter incorrectly handles gcloud bearer tokens
2. Bug: OpenRouter adapter uses wrong model IDs with OpenAI CLI
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
import httpx

from llm_council.adapters.gemini_adapter import GeminiAdapter
from llm_council.adapters.openrouter_adapter import OpenRouterAdapter
from llm_council.auth import CLISession, CLIProvider


class TestGeminiBearerTokenBug:
    """
    Bug: Gemini adapter treats gcloud OAuth tokens as API keys

    Problem: gcloud returns bearer tokens but adapter sends them
    in x-goog-api-key header instead of Authorization: Bearer

    Expected: Use Authorization: Bearer header for gcloud tokens
    """

    @pytest.mark.asyncio
    async def test_gcloud_token_uses_bearer_auth_header(self):
        """
        FAILING TEST: gcloud tokens should use Authorization: Bearer header

        This test will fail until we fix the Gemini adapter to detect
        bearer tokens and use the correct header.
        """
        config = {
            'display_name': 'Test Gemini',
            'use_cli_auth': True
        }
        adapter = GeminiAdapter(config)

        # Simulate gcloud CLI returning a bearer token
        mock_session = CLISession(
            provider=CLIProvider.GOOGLE_AI,
            token="ya29.test-gcloud-bearer-token",  # gcloud OAuth token format
            is_authenticated=True
        )

        with patch.object(adapter.cli_session_manager, 'get_session', return_value=mock_session):
            # Authenticate via gcloud
            result = adapter._authenticate_via_cli()
            assert result is True

            # Now query and verify the correct header is used
            with patch('httpx.AsyncClient') as mock_client:
                mock_response = Mock()
                mock_response.json.return_value = {
                    'candidates': [{
                        'content': {'parts': [{'text': 'Test response'}]}
                    }],
                    'usageMetadata': {'totalTokenCount': 100}
                }
                mock_response.status_code = 200

                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await adapter.query("Test prompt")

                # Verify the request used Authorization: Bearer header
                call_args = mock_post.call_args
                headers = call_args[1]['headers']

                # This assertion WILL FAIL with current code
                assert 'Authorization' in headers, "Missing Authorization header for bearer token"
                assert headers['Authorization'] == 'Bearer ya29.test-gcloud-bearer-token'

                # This should NOT be present for bearer tokens
                assert 'x-goog-api-key' not in headers or headers.get('x-goog-api-key') != mock_session.token

    @pytest.mark.asyncio
    async def test_api_key_still_uses_api_key_header(self):
        """
        Ensure API keys (not bearer tokens) still use x-goog-api-key header

        This verifies we don't break existing API key auth.
        """
        config = {
            'display_name': 'Test Gemini',
            'use_cli_auth': False
        }
        adapter = GeminiAdapter(config)

        with patch.dict('os.environ', {'GOOGLE_API_KEY': 'AIzaSyTest-api-key'}):
            result = adapter._authenticate_via_api_key()
            assert result is True

            with patch('httpx.AsyncClient') as mock_client:
                mock_response = Mock()
                mock_response.json.return_value = {
                    'candidates': [{
                        'content': {'parts': [{'text': 'Test response'}]}
                    }]
                }
                mock_response.status_code = 200

                mock_post = AsyncMock(return_value=mock_response)
                mock_client.return_value.__aenter__.return_value.post = mock_post

                await adapter.query("Test prompt")

                # API keys should use x-goog-api-key header
                call_args = mock_post.call_args
                headers = call_args[1]['headers']

                assert 'x-goog-api-key' in headers
                assert headers['x-goog-api-key'] == 'AIzaSyTest-api-key'


class TestOpenRouterModelIDBug:
    """
    Bug: OpenRouter adapter uses OpenRouter model IDs with OpenAI base URL

    Problem: When using OpenAI CLI, adapter switches to api.openai.com
    but keeps model ID like "openai/gpt-4-turbo". OpenAI expects "gpt-4-turbo".

    Expected: Strip vendor prefix when using OpenAI base URL
    """

    @pytest.mark.asyncio
    async def test_openai_cli_strips_model_prefix(self):
        """
        FAILING TEST: OpenAI CLI should use normalized model IDs

        This test will fail until we fix the OpenRouter adapter to
        strip vendor prefixes when using OpenAI's base URL.
        """
        config = {
            'display_name': 'Test GPT-4',
            'model_id': 'openai/gpt-4-turbo',  # OpenRouter format
            'use_cli_auth': True
        }
        adapter = OpenRouterAdapter(config)

        # Simulate OpenAI CLI returning API key
        mock_session = CLISession(
            provider=CLIProvider.OPENAI,
            api_key="sk-test-openai-key",
            is_authenticated=True
        )

        with patch.object(adapter.cli_session_manager, 'get_session', return_value=mock_session):
            # Authenticate via OpenAI CLI
            result = adapter._authenticate_via_cli()
            assert result is True

            # Mock the OpenAI API call
            with patch('openai.AsyncOpenAI') as mock_openai:
                mock_client = AsyncMock()
                mock_completion = Mock()
                mock_completion.choices = [Mock(message=Mock(content="Test response"))]
                mock_completion.usage = Mock(total_tokens=100)
                mock_completion.model_dump.return_value = {}

                mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
                mock_openai.return_value = mock_client

                # Re-authenticate to get mocked client
                adapter.client = mock_client

                await adapter.query("Test prompt")

                # Verify the model ID was normalized (prefix stripped)
                call_args = mock_client.chat.completions.create.call_args
                model_used = call_args[1]['model']

                # This assertion WILL FAIL with current code
                assert model_used == 'gpt-4-turbo', f"Expected 'gpt-4-turbo', got '{model_used}'"
                assert '/' not in model_used, "Model ID should not contain vendor prefix for OpenAI"

    @pytest.mark.asyncio
    async def test_openrouter_keeps_model_prefix(self):
        """
        Ensure OpenRouter base URL keeps vendor-prefixed model IDs

        This verifies we don't break OpenRouter when using their API.
        """
        config = {
            'display_name': 'Test GPT-4',
            'model_id': 'openai/gpt-4-turbo',
            'use_cli_auth': False
        }
        adapter = OpenRouterAdapter(config)

        with patch.dict('os.environ', {'OPENROUTER_API_KEY': 'sk-or-test-key'}):
            result = adapter._authenticate_via_api_key()
            assert result is True

            # Mock the OpenRouter API call
            with patch('openai.AsyncOpenAI') as mock_openai:
                mock_client = AsyncMock()
                mock_completion = Mock()
                mock_completion.choices = [Mock(message=Mock(content="Test response"))]
                mock_completion.usage = Mock(total_tokens=100)
                mock_completion.model_dump.return_value = {}

                mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
                mock_openai.return_value = mock_client
                adapter.client = mock_client

                await adapter.query("Test prompt")

                # OpenRouter should keep the vendor prefix
                call_args = mock_client.chat.completions.create.call_args
                model_used = call_args[1]['model']

                assert model_used == 'openai/gpt-4-turbo'
                assert '/' in model_used, "OpenRouter model IDs should keep vendor prefix"

    def test_grok_model_rejected_with_openai_cli(self):
        """
        Test that Grok models are properly handled with OpenAI CLI

        Grok (x-ai/grok-beta) is not available via OpenAI, so this
        should either fail gracefully or skip CLI auth.
        """
        config = {
            'display_name': 'Test Grok',
            'model_id': 'x-ai/grok-beta',  # Grok is not available via OpenAI
            'use_cli_auth': True
        }
        adapter = OpenRouterAdapter(config)

        # Simulate OpenAI CLI (which doesn't support Grok)
        mock_session = CLISession(
            provider=CLIProvider.OPENAI,
            api_key="sk-test-openai-key",
            is_authenticated=True
        )

        with patch.object(adapter.cli_session_manager, 'get_session', return_value=mock_session):
            # For now, we expect this to authenticate but note the incompatibility
            # In the future, could add validation to skip OpenAI CLI for Grok models
            result = adapter._authenticate_via_cli()

            # Current behavior: authenticates but will fail on query
            # Better behavior: detect incompatibility and skip this auth method
            # For now, just document this edge case
            assert result is True  # Current behavior

            # TODO: Consider adding model compatibility check


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])

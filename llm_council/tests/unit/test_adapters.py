"""Unit tests for LLM Adapters"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from adapters.base import BaseLLMAdapter, AuthMethod, LLMResponse
from adapters.claude_adapter import ClaudeAdapter
from adapters.gemini_adapter import GeminiAdapter
from adapters.openrouter_adapter import OpenRouterAdapter


class TestBaseLLMAdapter:
    """Test base adapter functionality"""

    def test_base_adapter_initialization(self, mock_config):
        """Test base adapter cannot be instantiated directly"""
        adapter_config = mock_config['models']['claude']

        # BaseLLMAdapter is abstract, should work when subclassed
        class TestAdapter(BaseLLMAdapter):
            def authenticate(self, method=AuthMethod.API_KEY):
                return True

            async def query(self, prompt, **kwargs):
                return LLMResponse(
                    model_name=self.model_name,
                    content="Test response"
                )

        adapter = TestAdapter(adapter_config)
        assert adapter.model_name == "Claude Sonnet 4.5"
        assert adapter.weight == 1.2

    def test_is_available_no_auth(self, mock_config):
        """Test is_available when not authenticated"""
        class TestAdapter(BaseLLMAdapter):
            def authenticate(self, method=AuthMethod.API_KEY):
                return False

            async def query(self, prompt, **kwargs):
                return LLMResponse(model_name=self.model_name, content="test")

        adapter = TestAdapter(mock_config['models']['claude'])
        assert adapter.is_available() == False


class TestClaudeAdapter:
    """Test Claude adapter"""

    def test_claude_initialization(self, mock_config):
        """Test Claude adapter initialization"""
        adapter = ClaudeAdapter(mock_config['models']['claude'])
        assert adapter.model_name == "Claude Sonnet 4.5"
        assert adapter.weight == 1.2
        assert adapter.client is None

    def test_claude_authentication_no_key(self, mock_config):
        """Test Claude authentication without API key"""
        adapter = ClaudeAdapter(mock_config['models']['claude'])

        # Mock missing environment variable
        with patch.dict(os.environ, {}, clear=True):
            result = adapter.authenticate()
            assert result == False
            assert adapter.client is None

    def test_claude_authentication_with_key(self, mock_config):
        """Test Claude authentication with valid API key"""
        adapter = ClaudeAdapter(mock_config['models']['claude'])

        # Mock environment variable
        with patch.dict(os.environ, {'ANTHROPIC_API_KEY': 'test-key-123'}):
            with patch('adapters.claude_adapter.AsyncAnthropic') as mock_anthropic:
                result = adapter.authenticate()
                assert result == True
                assert adapter.api_key == 'test-key-123'
                mock_anthropic.assert_called_once_with(api_key='test-key-123')

    @pytest.mark.asyncio
    async def test_claude_query_success(self, mock_config):
        """Test successful Claude query"""
        adapter = ClaudeAdapter(mock_config['models']['claude'])

        # Mock client and response
        mock_message = Mock()
        mock_message.content = [Mock(text="The answer is 4")]
        mock_message.usage = Mock(input_tokens=10, output_tokens=20)

        adapter.client = AsyncMock()
        adapter.client.messages.create = AsyncMock(return_value=mock_message)

        # Execute query
        response = await adapter.query("What is 2+2?")

        # Verify response
        assert response.success == True
        assert response.model_name == "Claude Sonnet 4.5"
        assert "4" in response.content
        assert response.tokens_used == 30

    @pytest.mark.asyncio
    async def test_claude_query_no_client(self, mock_config):
        """Test Claude query without authenticated client"""
        adapter = ClaudeAdapter(mock_config['models']['claude'])
        adapter.client = None

        # Mock failed authentication
        with patch.object(adapter, 'authenticate', return_value=False):
            response = await adapter.query("Test")

            assert response.success == False
            assert response.error == "Authentication failed"


class TestGeminiAdapter:
    """Test Gemini adapter"""

    def test_gemini_initialization(self, mock_config):
        """Test Gemini adapter initialization"""
        adapter = GeminiAdapter(mock_config['models']['gemini'])
        assert adapter.model_name == "Gemini 1.5 Flash"
        assert adapter.weight == 1.0
        assert adapter.client is None

    def test_gemini_authentication_no_key(self, mock_config):
        """Test Gemini authentication without API key"""
        adapter = GeminiAdapter(mock_config['models']['gemini'])

        with patch.dict(os.environ, {}, clear=True):
            result = adapter.authenticate()
            assert result == False

    def test_gemini_authentication_with_key(self, mock_config):
        """Test Gemini authentication with valid API key"""
        adapter = GeminiAdapter(mock_config['models']['gemini'])

        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test-gemini-key'}):
            with patch('adapters.gemini_adapter.genai') as mock_genai:
                mock_model = Mock()
                mock_genai.GenerativeModel.return_value = mock_model

                result = adapter.authenticate()

                assert result == True
                assert adapter.api_key == 'test-gemini-key'
                mock_genai.configure.assert_called_once()

    @pytest.mark.asyncio
    async def test_gemini_query_success(self, mock_config):
        """Test successful Gemini query"""
        adapter = GeminiAdapter(mock_config['models']['gemini'])

        # Mock response
        mock_response = Mock()
        mock_response.text = "The answer is 4"
        mock_response.usage_metadata = Mock(
            prompt_token_count=8,
            candidates_token_count=15
        )

        adapter.client = Mock()
        adapter.client.generate_content = Mock(return_value=mock_response)

        # Execute query (will be wrapped in asyncio.to_thread)
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            mock_thread.return_value = mock_response
            response = await adapter.query("What is 2+2?")

            assert response.success == True
            assert "4" in response.content
            assert response.tokens_used == 23

    @pytest.mark.asyncio
    async def test_gemini_query_error(self, mock_config):
        """Test Gemini query with error"""
        adapter = GeminiAdapter(mock_config['models']['gemini'])
        adapter.client = Mock()

        # Mock exception
        with patch('asyncio.to_thread', new_callable=AsyncMock) as mock_thread:
            mock_thread.side_effect = Exception("API Error")
            response = await adapter.query("Test")

            assert response.success == False
            assert "API Error" in response.error


class TestOpenRouterAdapter:
    """Test OpenRouter adapter"""

    def test_openrouter_initialization(self, mock_config):
        """Test OpenRouter adapter initialization"""
        adapter = OpenRouterAdapter(mock_config['models']['gpt4'])
        assert adapter.model_name == "GPT-4 Turbo"
        assert adapter.weight == 1.1
        assert adapter.client is None

    def test_openrouter_authentication_no_key(self, mock_config):
        """Test OpenRouter authentication without API key"""
        adapter = OpenRouterAdapter(mock_config['models']['gpt4'])

        with patch.dict(os.environ, {}, clear=True):
            result = adapter.authenticate()
            assert result == False

    def test_openrouter_authentication_with_key(self, mock_config):
        """Test OpenRouter authentication with valid API key"""
        adapter = OpenRouterAdapter(mock_config['models']['gpt4'])

        with patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-or-key'}):
            with patch('adapters.openrouter_adapter.AsyncOpenAI') as mock_openai:
                result = adapter.authenticate()

                assert result == True
                assert adapter.api_key == 'test-or-key'
                mock_openai.assert_called_once()

    @pytest.mark.asyncio
    async def test_openrouter_query_success(self, mock_config):
        """Test successful OpenRouter query"""
        adapter = OpenRouterAdapter(mock_config['models']['gpt4'])

        # Mock response
        mock_message = Mock()
        mock_message.content = "Four"
        mock_choice = Mock(message=mock_message)
        mock_response = Mock()
        mock_response.choices = [mock_choice]
        mock_response.usage = Mock(total_tokens=25)

        adapter.client = AsyncMock()
        adapter.client.chat.completions.create = AsyncMock(return_value=mock_response)

        # Execute query
        response = await adapter.query("What is 2+2?")

        assert response.success == True
        assert response.content == "Four"
        assert response.tokens_used == 25


class TestAdapterFactory:
    """Test adapter creation and configuration"""

    def test_all_adapters_implement_interface(self, mock_config):
        """Test that all adapters implement required interface"""
        adapters = [
            ClaudeAdapter(mock_config['models']['claude']),
            GeminiAdapter(mock_config['models']['gemini']),
            OpenRouterAdapter(mock_config['models']['gpt4'])
        ]

        for adapter in adapters:
            # Check required methods exist
            assert hasattr(adapter, 'authenticate')
            assert hasattr(adapter, 'query')
            assert hasattr(adapter, 'is_available')

            # Check required attributes
            assert hasattr(adapter, 'model_name')
            assert hasattr(adapter, 'weight')

    def test_adapter_weights(self, mock_config):
        """Test that adapter weights are correctly set"""
        claude = ClaudeAdapter(mock_config['models']['claude'])
        gemini = GeminiAdapter(mock_config['models']['gemini'])
        gpt4 = OpenRouterAdapter(mock_config['models']['gpt4'])

        assert claude.weight == 1.2
        assert gemini.weight == 1.0
        assert gpt4.weight == 1.1

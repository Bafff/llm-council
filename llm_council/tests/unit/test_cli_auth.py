"""Tests for CLI authentication system"""

import pytest
import os
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import json

from llm_council.auth import CLISessionManager, CLIProvider, CLISession


class TestCLISessionManager:
    """Test CLISessionManager functionality"""

    def test_initialization(self):
        """Test CLI session manager initialization"""
        manager = CLISessionManager()
        assert manager.home_dir == Path.home()
        assert manager._session_cache == {}

    def test_get_session_with_cache(self):
        """Test session caching"""
        manager = CLISessionManager()

        # Create a mock session
        mock_session = CLISession(
            provider=CLIProvider.CLAUDE_CODE,
            is_authenticated=True,
            token="test-token"
        )

        # Add to cache
        manager._session_cache[CLIProvider.CLAUDE_CODE] = mock_session

        # Get session with cache enabled
        session = manager.get_session(CLIProvider.CLAUDE_CODE, use_cache=True)
        assert session.is_authenticated
        assert session.token == "test-token"

    def test_get_session_without_cache(self):
        """Test session retrieval without cache"""
        manager = CLISessionManager()

        # Add to cache
        manager._session_cache[CLIProvider.CLAUDE_CODE] = CLISession(
            provider=CLIProvider.CLAUDE_CODE,
            is_authenticated=True,
            token="cached-token"
        )

        # Get session without cache (should fetch fresh)
        with patch.object(manager, '_get_claude_code_session') as mock_fetch:
            mock_fetch.return_value = CLISession(
                provider=CLIProvider.CLAUDE_CODE,
                is_authenticated=True,
                token="fresh-token"
            )

            session = manager.get_session(CLIProvider.CLAUDE_CODE, use_cache=False)
            mock_fetch.assert_called_once()
            assert session.token == "fresh-token"

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        'sessionKey': 'test-session-key'
    }))
    @patch('pathlib.Path.exists')
    def test_get_claude_code_session_success(self, mock_exists, mock_file):
        """Test successful Claude Code session extraction"""
        mock_exists.return_value = True

        manager = CLISessionManager()
        session = manager._get_claude_code_session()

        assert session.is_authenticated
        assert session.token == 'test-session-key'
        assert session.provider == CLIProvider.CLAUDE_CODE

    @patch('os.getenv')
    def test_get_claude_code_session_from_env(self, mock_getenv):
        """Test Claude Code session from environment variable"""
        mock_getenv.return_value = 'env-session-token'

        manager = CLISessionManager()
        session = manager._get_claude_code_session()

        assert session.is_authenticated
        assert session.token == 'env-session-token'
        mock_getenv.assert_called_with('CLAUDE_CODE_SESSION')

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        'api_key': 'test-api-key'
    }))
    @patch('pathlib.Path.exists')
    def test_get_anthropic_cli_session(self, mock_exists, mock_file):
        """Test Anthropic CLI session extraction"""
        mock_exists.return_value = True

        manager = CLISessionManager()
        session = manager._get_anthropic_cli_session()

        assert session.is_authenticated
        assert session.api_key == 'test-api-key'

    @patch('builtins.open', new_callable=mock_open, read_data='OPENAI_API_KEY="test-openai-key"')
    @patch('pathlib.Path.exists')
    def test_get_chatgpt_session_sgpt(self, mock_exists, mock_file):
        """Test ChatGPT session extraction from shell_gpt"""
        mock_exists.return_value = True

        manager = CLISessionManager()
        session = manager._get_chatgpt_session()

        assert session.is_authenticated
        assert session.api_key == 'test-openai-key'

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        'api_key': 'gemini-api-key'
    }))
    @patch('pathlib.Path.exists')
    def test_get_gemini_session(self, mock_exists, mock_file):
        """Test Gemini session extraction"""
        mock_exists.return_value = True

        manager = CLISessionManager()
        session = manager._get_gemini_session()

        assert session.is_authenticated
        assert session.api_key == 'gemini-api-key'

    @patch('subprocess.run')
    @patch('pathlib.Path.exists')
    def test_get_google_ai_session_gcloud(self, mock_exists, mock_run):
        """Test Google AI session extraction via gcloud"""
        mock_exists.return_value = False  # No config file

        # Mock gcloud CLI response
        mock_run.return_value = Mock(
            returncode=0,
            stdout='gcloud-access-token\n'
        )

        with patch.object(CLISessionManager, '_find_cli_tool', return_value='/usr/bin/gcloud'):
            manager = CLISessionManager()
            session = manager._get_google_ai_session()

            assert session.is_authenticated
            assert session.token == 'gcloud-access-token'

    @patch('subprocess.run')
    def test_find_cli_tool_success(self, mock_run):
        """Test successful CLI tool detection"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout='/usr/local/bin/claude\n'
        )

        manager = CLISessionManager()
        path = manager._find_cli_tool(['claude'])

        assert path == '/usr/local/bin/claude'

    @patch('subprocess.run')
    def test_find_cli_tool_not_found(self, mock_run):
        """Test CLI tool not found"""
        mock_run.return_value = Mock(
            returncode=1,
            stdout=''
        )

        manager = CLISessionManager()
        path = manager._find_cli_tool(['nonexistent-tool'])

        assert path is None

    def test_is_cli_available_true(self):
        """Test CLI availability check - available"""
        manager = CLISessionManager()

        mock_session = CLISession(
            provider=CLIProvider.CLAUDE_CODE,
            is_authenticated=True
        )

        with patch.object(manager, 'get_session', return_value=mock_session):
            assert manager.is_cli_available(CLIProvider.CLAUDE_CODE) is True

    def test_is_cli_available_false(self):
        """Test CLI availability check - unavailable"""
        manager = CLISessionManager()

        mock_session = CLISession(
            provider=CLIProvider.CLAUDE_CODE,
            is_authenticated=False
        )

        with patch.object(manager, 'get_session', return_value=mock_session):
            assert manager.is_cli_available(CLIProvider.CLAUDE_CODE) is False

    def test_clear_cache(self):
        """Test cache clearing"""
        manager = CLISessionManager()

        # Add some cached data
        manager._session_cache[CLIProvider.CLAUDE_CODE] = CLISession(
            provider=CLIProvider.CLAUDE_CODE,
            is_authenticated=True
        )

        assert len(manager._session_cache) == 1

        # Clear cache
        manager.clear_cache()

        assert len(manager._session_cache) == 0


class TestCLISession:
    """Test CLISession dataclass"""

    def test_session_creation(self):
        """Test creating a CLI session"""
        session = CLISession(
            provider=CLIProvider.CLAUDE_CODE,
            token="test-token",
            is_authenticated=True
        )

        assert session.provider == CLIProvider.CLAUDE_CODE
        assert session.token == "test-token"
        assert session.is_authenticated is True
        assert session.api_key is None

    def test_session_with_api_key(self):
        """Test session with API key"""
        session = CLISession(
            provider=CLIProvider.OPENAI,
            api_key="sk-test-key",
            is_authenticated=True
        )

        assert session.api_key == "sk-test-key"
        assert session.token is None


class TestCLIProvider:
    """Test CLIProvider enum"""

    def test_provider_values(self):
        """Test all provider enum values"""
        assert CLIProvider.CLAUDE_CODE.value == "claude_code"
        assert CLIProvider.ANTHROPIC.value == "anthropic"
        assert CLIProvider.CHATGPT.value == "chatgpt"
        assert CLIProvider.OPENAI.value == "openai"
        assert CLIProvider.GEMINI.value == "gemini"
        assert CLIProvider.GOOGLE_AI.value == "google_ai"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

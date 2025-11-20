"""
CLI Session Manager - Detects and extracts authentication tokens from CLI tools.

This module provides a unified interface to leverage existing CLI tool subscriptions
(Claude Code CLI, ChatGPT CLI, Gemini CLI, etc.) instead of requiring API keys.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class CLIProvider(Enum):
    """Supported CLI providers"""
    CLAUDE_CODE = "claude_code"
    ANTHROPIC = "anthropic"
    CHATGPT = "chatgpt"
    OPENAI = "openai"
    GEMINI = "gemini"
    GOOGLE_AI = "google_ai"


@dataclass
class CLISession:
    """Represents an authenticated CLI session"""
    provider: CLIProvider
    token: Optional[str] = None
    api_key: Optional[str] = None
    session_data: Optional[Dict[str, Any]] = None
    is_authenticated: bool = False
    cli_tool_path: Optional[str] = None


class CLISessionManager:
    """
    Manages authentication across various CLI tools.

    Detects installed CLI tools and extracts authentication tokens
    to use existing subscriptions instead of API keys.
    """

    def __init__(self):
        self.home_dir = Path.home()
        self._session_cache: Dict[CLIProvider, CLISession] = {}

    def get_session(self, provider: CLIProvider, use_cache: bool = True) -> CLISession:
        """
        Get an authenticated session for the specified provider.

        Args:
            provider: The CLI provider to get session for
            use_cache: Whether to use cached session data

        Returns:
            CLISession object with authentication details
        """
        if use_cache and provider in self._session_cache:
            return self._session_cache[provider]

        session = None

        if provider == CLIProvider.CLAUDE_CODE:
            session = self._get_claude_code_session()
        elif provider == CLIProvider.ANTHROPIC:
            session = self._get_anthropic_cli_session()
        elif provider == CLIProvider.CHATGPT:
            session = self._get_chatgpt_session()
        elif provider == CLIProvider.OPENAI:
            session = self._get_openai_cli_session()
        elif provider == CLIProvider.GEMINI:
            session = self._get_gemini_session()
        elif provider == CLIProvider.GOOGLE_AI:
            session = self._get_google_ai_session()
        else:
            session = CLISession(provider=provider, is_authenticated=False)

        self._session_cache[provider] = session
        return session

    def _get_claude_code_session(self) -> CLISession:
        """
        Extract authentication from Claude Code CLI.

        Checks for:
        1. Running in Claude Code context (environment variables)
        2. Claude Code CLI session files
        3. Anthropic CLI configuration
        """
        session = CLISession(provider=CLIProvider.CLAUDE_CODE)

        # Check if running inside Claude Code context
        if os.getenv('CLAUDE_CODE_SESSION'):
            session.token = os.getenv('CLAUDE_CODE_SESSION')
            session.is_authenticated = True
            return session

        # Check for Claude Code CLI session files
        claude_config_paths = [
            self.home_dir / '.claude' / 'session.json',
            self.home_dir / '.config' / 'claude' / 'session.json',
            self.home_dir / '.anthropic' / 'session.json',
        ]

        for config_path in claude_config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        session_data = json.load(f)
                        session.session_data = session_data

                        # Extract token from various possible fields
                        session.token = (
                            session_data.get('sessionKey') or
                            session_data.get('session_key') or
                            session_data.get('api_key') or
                            session_data.get('token')
                        )

                        if session.token:
                            session.is_authenticated = True
                            return session
                except (json.JSONDecodeError, IOError):
                    continue

        # Try to detect Claude CLI tool
        cli_path = self._find_cli_tool(['claude', 'anthropic'])
        if cli_path:
            session.cli_tool_path = cli_path
            # Try to extract session using CLI command
            token = self._extract_token_from_cli(cli_path, ['session', 'show'])
            if token:
                session.token = token
                session.is_authenticated = True

        return session

    def _get_anthropic_cli_session(self) -> CLISession:
        """Extract authentication from Anthropic CLI"""
        session = CLISession(provider=CLIProvider.ANTHROPIC)

        # Check for Anthropic CLI config
        anthropic_config_paths = [
            self.home_dir / '.anthropic' / 'config.json',
            self.home_dir / '.config' / 'anthropic' / 'config.json',
        ]

        for config_path in anthropic_config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                        session.api_key = config_data.get('api_key')
                        if session.api_key:
                            session.is_authenticated = True
                            return session
                except (json.JSONDecodeError, IOError):
                    continue

        return session

    def _get_chatgpt_session(self) -> CLISession:
        """
        Extract authentication from ChatGPT CLI.

        Supports various ChatGPT CLI implementations:
        - Official OpenAI CLI
        - shell_gpt
        - chatgpt-cli
        """
        session = CLISession(provider=CLIProvider.CHATGPT)

        # Check for shell_gpt config
        sgpt_config = self.home_dir / '.config' / 'shell_gpt' / '.sgptrc'
        if sgpt_config.exists():
            try:
                with open(sgpt_config, 'r') as f:
                    for line in f:
                        if line.startswith('OPENAI_API_KEY='):
                            session.api_key = line.split('=', 1)[1].strip().strip('"\'')
                            session.is_authenticated = True
                            return session
            except IOError:
                pass

        # Check for chatgpt-cli config
        chatgpt_config = self.home_dir / '.config' / 'chatgpt' / 'config.json'
        if chatgpt_config.exists():
            try:
                with open(chatgpt_config, 'r') as f:
                    config_data = json.load(f)
                    session.token = config_data.get('session_token')
                    session.api_key = config_data.get('api_key')
                    if session.token or session.api_key:
                        session.is_authenticated = True
                        return session
            except (json.JSONDecodeError, IOError):
                pass

        # Try to detect ChatGPT CLI tool
        cli_path = self._find_cli_tool(['chatgpt', 'sgpt'])
        if cli_path:
            session.cli_tool_path = cli_path

        return session

    def _get_openai_cli_session(self) -> CLISession:
        """Extract authentication from OpenAI CLI"""
        session = CLISession(provider=CLIProvider.OPENAI)

        # Check for OpenAI CLI config
        openai_config_paths = [
            self.home_dir / '.openai' / 'config.json',
            self.home_dir / '.config' / 'openai' / 'config.json',
        ]

        for config_path in openai_config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                        session.api_key = config_data.get('api_key')
                        if session.api_key:
                            session.is_authenticated = True
                            return session
                except (json.JSONDecodeError, IOError):
                    continue

        # Try to detect OpenAI CLI tool
        cli_path = self._find_cli_tool(['openai'])
        if cli_path:
            session.cli_tool_path = cli_path

        return session

    def _get_gemini_session(self) -> CLISession:
        """Extract authentication from Gemini CLI"""
        session = CLISession(provider=CLIProvider.GEMINI)

        # Check for Google AI Studio / Gemini config
        gemini_config_paths = [
            self.home_dir / '.gemini' / 'config.json',
            self.home_dir / '.config' / 'gemini' / 'config.json',
            self.home_dir / '.config' / 'gcloud' / 'application_default_credentials.json',
        ]

        for config_path in gemini_config_paths:
            if config_path.exists():
                try:
                    with open(config_path, 'r') as f:
                        config_data = json.load(f)
                        session.api_key = (
                            config_data.get('api_key') or
                            config_data.get('client_id')  # For OAuth
                        )
                        if session.api_key:
                            session.is_authenticated = True
                            session.session_data = config_data
                            return session
                except (json.JSONDecodeError, IOError):
                    continue

        return session

    def _get_google_ai_session(self) -> CLISession:
        """Extract authentication from Google Cloud CLI (gcloud)"""
        session = CLISession(provider=CLIProvider.GOOGLE_AI)

        # Check for gcloud credentials
        gcloud_config = self.home_dir / '.config' / 'gcloud' / 'application_default_credentials.json'
        if gcloud_config.exists():
            try:
                with open(gcloud_config, 'r') as f:
                    config_data = json.load(f)
                    session.session_data = config_data
                    session.token = config_data.get('token') or config_data.get('access_token')
                    if session.token:
                        session.is_authenticated = True
                        return session
            except (json.JSONDecodeError, IOError):
                pass

        # Try to get access token from gcloud CLI
        cli_path = self._find_cli_tool(['gcloud'])
        if cli_path:
            session.cli_tool_path = cli_path
            try:
                result = subprocess.run(
                    [cli_path, 'auth', 'print-access-token'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0 and result.stdout.strip():
                    session.token = result.stdout.strip()
                    session.is_authenticated = True
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                pass

        return session

    def _find_cli_tool(self, tool_names: list) -> Optional[str]:
        """
        Find CLI tool in system PATH.

        Args:
            tool_names: List of possible tool names to search for

        Returns:
            Path to CLI tool if found, None otherwise
        """
        for tool_name in tool_names:
            try:
                result = subprocess.run(
                    ['which', tool_name],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, subprocess.SubprocessError):
                continue
        return None

    def _extract_token_from_cli(self, cli_path: str, args: list) -> Optional[str]:
        """
        Try to extract authentication token by running CLI command.

        Args:
            cli_path: Path to CLI tool
            args: Command arguments

        Returns:
            Extracted token if successful, None otherwise
        """
        try:
            result = subprocess.run(
                [cli_path] + args,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                # Try to parse as JSON
                try:
                    data = json.loads(result.stdout)
                    return data.get('token') or data.get('session_key') or data.get('api_key')
                except json.JSONDecodeError:
                    # Return raw output if not JSON
                    output = result.stdout.strip()
                    return output if output else None
        except (subprocess.TimeoutExpired, subprocess.SubprocessError):
            pass
        return None

    def is_cli_available(self, provider: CLIProvider) -> bool:
        """
        Check if CLI tool is available and authenticated.

        Args:
            provider: The CLI provider to check

        Returns:
            True if CLI is available and authenticated, False otherwise
        """
        session = self.get_session(provider)
        return session.is_authenticated

    def clear_cache(self):
        """Clear cached session data"""
        self._session_cache.clear()

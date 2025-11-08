"""Claude adapter with multiple auth methods"""

import os
import time
from typing import Optional
from anthropic import Anthropic, AsyncAnthropic

from .base import BaseLLMAdapter, LLMResponse, AuthMethod
from ..auth import CLISessionManager, CLIProvider


class ClaudeAdapter(BaseLLMAdapter):
    """Adapter for Claude via Anthropic API"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.client: Optional[AsyncAnthropic] = None
        self.api_key: Optional[str] = None
        self.model = "claude-sonnet-4-20250514"  # Latest Sonnet
        self.cli_session_manager = CLISessionManager()
        self.use_cli_auth = config.get('use_cli_auth', True)  # Default: try CLI first

    def authenticate(self, method: AuthMethod = AuthMethod.CLI_SESSION) -> bool:
        """
        Authenticate with Claude using CLI session or API key.

        Tries CLI authentication first (if enabled), falls back to API key.
        """
        # Try CLI session authentication first (if enabled)
        if self.use_cli_auth and method == AuthMethod.CLI_SESSION:
            if self._authenticate_via_cli():
                return True
            # Fall back to API key if CLI auth fails
            print(f"ℹ️  {self.model_name}: CLI auth unavailable, trying API key...")
            method = AuthMethod.API_KEY

        if method == AuthMethod.API_KEY:
            return self._authenticate_via_api_key()

        elif method == AuthMethod.CLAUDE_CODE_SESSION:
            # Legacy method, redirect to CLI_SESSION
            return self._authenticate_via_cli()

        elif method == AuthMethod.BROWSER_COOKIES:
            print(f"⚠️  {self.model_name}: Browser cookie auth not yet implemented")
            return False

        return False

    def _authenticate_via_cli(self) -> bool:
        """Authenticate using Claude Code or Anthropic CLI session"""
        try:
            # Try Claude Code CLI first
            session = self.cli_session_manager.get_session(CLIProvider.CLAUDE_CODE)
            if session.is_authenticated:
                self.api_key = session.token or session.api_key
                if self.api_key:
                    self.client = AsyncAnthropic(api_key=self.api_key)
                    self.auth_method_used = "CLI Session"
                    self.auth_source = "Claude Code CLI"
                    print(f"✅ {self.model_name}: Authenticated via Claude Code CLI")
                    return True

            # Try Anthropic CLI
            session = self.cli_session_manager.get_session(CLIProvider.ANTHROPIC)
            if session.is_authenticated and session.api_key:
                self.api_key = session.api_key
                self.client = AsyncAnthropic(api_key=self.api_key)
                self.auth_method_used = "CLI Session"
                self.auth_source = "Anthropic CLI"
                print(f"✅ {self.model_name}: Authenticated via Anthropic CLI")
                return True

        except Exception as e:
            print(f"⚠️  {self.model_name}: CLI auth failed - {e}")

        return False

    def _authenticate_via_api_key(self) -> bool:
        """Authenticate using API key from environment"""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')

        if not self.api_key:
            print(f"⚠️  {self.model_name}: No API key found (set ANTHROPIC_API_KEY)")
            return False

        try:
            self.client = AsyncAnthropic(api_key=self.api_key)
            self.auth_method_used = "API Key"
            self.auth_source = "ANTHROPIC_API_KEY env var"
            print(f"✅ {self.model_name}: Authenticated via API key")
            return True
        except Exception as e:
            print(f"❌ {self.model_name}: Auth failed - {e}")
            return False

    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Query Claude"""
        if not self.client:
            if not self.authenticate():
                return LLMResponse(
                    model_name=self.model_name,
                    content="",
                    error="Authentication failed"
                )

        start_time = time.time()

        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=kwargs.get('max_tokens', 4096),
                temperature=kwargs.get('temperature', 0.7),
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                model_name=self.model_name,
                content=message.content[0].text,
                confidence=0.9,  # Claude typically high quality
                tokens_used=message.usage.input_tokens + message.usage.output_tokens,
                latency_ms=latency,
                raw_response=message.model_dump(),
                auth_method=self.auth_method_used,
                auth_source=self.auth_source
            )

        except Exception as e:
            return LLMResponse(
                model_name=self.model_name,
                content="",
                error=f"Query failed: {str(e)}"
            )

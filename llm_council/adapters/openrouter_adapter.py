"""OpenRouter adapter - access to GPT-4, Grok, and 100+ models"""

import os
import time
from typing import Optional
from openai import AsyncOpenAI

from .base import BaseLLMAdapter, LLMResponse, AuthMethod
from ..auth import CLISessionManager, CLIProvider


class OpenRouterAdapter(BaseLLMAdapter):
    """Adapter for OpenRouter (GPT-4, Grok, etc.)"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.client: Optional[AsyncOpenAI] = None
        self.api_key: Optional[str] = None
        self.model_id = config.get('model_id', 'openai/gpt-4-turbo')
        self.base_url: Optional[str] = None  # Track which API we're using
        self.cli_session_manager = CLISessionManager()
        self.use_cli_auth = config.get('use_cli_auth', True)  # Default: try CLI first

    def authenticate(self, method: AuthMethod = AuthMethod.CLI_SESSION) -> bool:
        """
        Authenticate with OpenRouter/OpenAI using CLI session or API key.

        Tries CLI authentication first (if enabled), falls back to API key.
        """
        if not self.use_cli_auth and method == AuthMethod.CLI_SESSION:
            method = AuthMethod.API_KEY

        # Try CLI session authentication first (if enabled)
        if self.use_cli_auth and method == AuthMethod.CLI_SESSION:
            if self._authenticate_via_cli():
                return True
            # Fall back to API key if CLI auth fails
            print(f"ℹ️  {self.model_name}: CLI auth unavailable, trying API key...")
            method = AuthMethod.API_KEY

        if method == AuthMethod.API_KEY:
            return self._authenticate_via_api_key()

        return False

    def _authenticate_via_cli(self) -> bool:
        """Authenticate using ChatGPT/OpenAI CLI session"""
        try:
            # Try ChatGPT CLI
            session = self.cli_session_manager.get_session(CLIProvider.CHATGPT)
            if session.is_authenticated and (session.api_key or session.token):
                if not self._is_model_supported_by_openai():
                    print(
                        f"⚠️  {self.model_name}: Model '{self.model_id}' is not available via OpenAI CLI auth"
                    )
                else:
                    self.api_key = session.api_key or session.token
                    self.base_url = "https://api.openai.com/v1"
                    self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
                    self.auth_method_used = "CLI Session"
                    self.auth_source = "ChatGPT CLI (sgpt)"
                    print(f"✅ {self.model_name}: Authenticated via ChatGPT CLI")
                    return True

            # Try OpenAI CLI
            session = self.cli_session_manager.get_session(CLIProvider.OPENAI)
            if session.is_authenticated and session.api_key:
                if not self._is_model_supported_by_openai():
                    print(
                        f"⚠️  {self.model_name}: Model '{self.model_id}' is not available via OpenAI CLI auth"
                    )
                else:
                    self.api_key = session.api_key
                    self.base_url = "https://api.openai.com/v1"
                    self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
                    self.auth_method_used = "CLI Session"
                    self.auth_source = "OpenAI CLI"
                    print(f"✅ {self.model_name}: Authenticated via OpenAI CLI")
                    return True

        except Exception as e:
            print(f"⚠️  {self.model_name}: CLI auth failed - {e}")

        return False

    def _authenticate_via_api_key(self) -> bool:
        """Authenticate using API key from environment"""
        # Try OpenRouter key first, then OpenAI key
        self.api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OPENAI_API_KEY')

        if not self.api_key:
            print(f"⚠️  {self.model_name}: No API key found")
            print("   Option 1: Get OpenRouter key (cheap): https://openrouter.ai/")
            print("   Option 2: Set OPENAI_API_KEY if you have OpenAI account")
            return False

        try:
            # OpenRouter uses OpenAI-compatible API
            self.base_url = "https://openrouter.ai/api/v1"
            auth_source = "OPENROUTER_API_KEY env var"

            if 'OPENAI_API_KEY' in os.environ and 'OPENROUTER_API_KEY' not in os.environ:
                self.base_url = "https://api.openai.com/v1"
                auth_source = "OPENAI_API_KEY env var"

            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
            self.auth_method_used = "API Key"
            self.auth_source = auth_source
            print(f"✅ {self.model_name}: Authenticated via API key")
            return True
        except Exception as e:
            print(f"❌ {self.model_name}: Auth failed - {e}")
            return False

    def _normalize_model_id(self) -> str:
        """
        Normalize model ID based on the base URL being used.

        OpenRouter uses vendor-prefixed model IDs (e.g., "openai/gpt-4-turbo")
        OpenAI API uses plain model names (e.g., "gpt-4-turbo")

        Returns:
            Normalized model ID for the current base URL
        """
        if self.base_url and "api.openai.com" in self.base_url:
            # Using OpenAI API - strip vendor prefix
            if '/' in self.model_id:
                # Extract model name after the prefix (e.g., "openai/gpt-4-turbo" -> "gpt-4-turbo")
                vendor, model = self.model_id.split('/', 1)
                if vendor != "openai":
                    raise ValueError(
                        f"Model '{self.model_id}' is not supported by the OpenAI API base URL"
                    )
                return model
            return self.model_id
        else:
            # Using OpenRouter - keep vendor prefix
            return self.model_id

    def _is_model_supported_by_openai(self) -> bool:
        """Return True if the configured model can be used with OpenAI's API."""
        if '/' not in self.model_id:
            return True
        vendor, _ = self.model_id.split('/', 1)
        return vendor == "openai"

    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Query OpenRouter model"""
        if not self.client:
            if not self.authenticate():
                return LLMResponse(
                    model_name=self.model_name,
                    content="",
                    error="Authentication failed"
                )

        start_time = time.time()

        try:
            # Normalize model ID based on which API we're using
            model_id = self._normalize_model_id()

            completion = await self.client.chat.completions.create(
                model=model_id,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=kwargs.get('max_tokens', 4096),
                temperature=kwargs.get('temperature', 0.7),
            )

            latency = (time.time() - start_time) * 1000

            return LLMResponse(
                model_name=self.model_name,
                content=completion.choices[0].message.content,
                confidence=0.88,
                tokens_used=completion.usage.total_tokens if completion.usage else None,
                latency_ms=latency,
                raw_response=completion.model_dump(),
                auth_method=self.auth_method_used,
                auth_source=self.auth_source
            )

        except Exception as e:
            return LLMResponse(
                model_name=self.model_name,
                content="",
                error=f"Query failed: {str(e)}"
            )

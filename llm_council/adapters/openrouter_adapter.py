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
        self.cli_session_manager = CLISessionManager()
        self.use_cli_auth = config.get('use_cli_auth', True)  # Default: try CLI first

    def authenticate(self, method: AuthMethod = AuthMethod.CLI_SESSION) -> bool:
        """
        Authenticate with OpenRouter/OpenAI using CLI session or API key.

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

        return False

    def _authenticate_via_cli(self) -> bool:
        """Authenticate using ChatGPT/OpenAI CLI session"""
        try:
            # Try ChatGPT CLI
            session = self.cli_session_manager.get_session(CLIProvider.CHATGPT)
            if session.is_authenticated and (session.api_key or session.token):
                self.api_key = session.api_key or session.token
                base_url = "https://api.openai.com/v1"
                self.client = AsyncOpenAI(api_key=self.api_key, base_url=base_url)
                print(f"✅ {self.model_name}: Authenticated via ChatGPT CLI")
                return True

            # Try OpenAI CLI
            session = self.cli_session_manager.get_session(CLIProvider.OPENAI)
            if session.is_authenticated and session.api_key:
                self.api_key = session.api_key
                base_url = "https://api.openai.com/v1"
                self.client = AsyncOpenAI(api_key=self.api_key, base_url=base_url)
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
            base_url = "https://openrouter.ai/api/v1"
            if 'OPENAI_API_KEY' in os.environ and 'OPENROUTER_API_KEY' not in os.environ:
                base_url = "https://api.openai.com/v1"

            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url=base_url
            )
            print(f"✅ {self.model_name}: Authenticated via API key")
            return True
        except Exception as e:
            print(f"❌ {self.model_name}: Auth failed - {e}")
            return False

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
            completion = await self.client.chat.completions.create(
                model=self.model_id,
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
                raw_response=completion.model_dump()
            )

        except Exception as e:
            return LLMResponse(
                model_name=self.model_name,
                content="",
                error=f"Query failed: {str(e)}"
            )

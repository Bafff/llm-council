"""Claude adapter with multiple auth methods"""

import os
import time
from typing import Optional
from anthropic import Anthropic, AsyncAnthropic

from .base import BaseLLMAdapter, LLMResponse, AuthMethod


class ClaudeAdapter(BaseLLMAdapter):
    """Adapter for Claude via Anthropic API"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.client: Optional[AsyncAnthropic] = None
        self.api_key: Optional[str] = None
        self.model = "claude-sonnet-4-20250514"  # Latest Sonnet

    def authenticate(self, method: AuthMethod = AuthMethod.API_KEY) -> bool:
        """Authenticate with Claude"""
        if method == AuthMethod.API_KEY:
            # Try environment variable first
            self.api_key = os.getenv('ANTHROPIC_API_KEY')

            if not self.api_key:
                print(f"⚠️  {self.model_name}: No API key found (set ANTHROPIC_API_KEY)")
                return False

            try:
                self.client = AsyncAnthropic(api_key=self.api_key)
                return True
            except Exception as e:
                print(f"❌ {self.model_name}: Auth failed - {e}")
                return False

        elif method == AuthMethod.CLAUDE_CODE_SESSION:
            # TODO: Implement Claude Code session extraction
            print(f"⚠️  {self.model_name}: Claude Code session auth not yet implemented")
            return False

        elif method == AuthMethod.BROWSER_COOKIES:
            # TODO: Implement browser cookie auth
            print(f"⚠️  {self.model_name}: Browser cookie auth not yet implemented")
            return False

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
                raw_response=message.model_dump()
            )

        except Exception as e:
            return LLMResponse(
                model_name=self.model_name,
                content="",
                error=f"Query failed: {str(e)}"
            )

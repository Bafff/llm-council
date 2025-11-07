"""OpenRouter adapter - access to GPT-4, Grok, and 100+ models"""

import os
import time
from typing import Optional
from openai import AsyncOpenAI

from llm_council.adapters.base import BaseLLMAdapter, LLMResponse, AuthMethod


class OpenRouterAdapter(BaseLLMAdapter):
    """Adapter for OpenRouter (GPT-4, Grok, etc.)"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.client: Optional[AsyncOpenAI] = None
        self.api_key: Optional[str] = None
        self.model_id = config.get('model_id', 'openai/gpt-4-turbo')

    def authenticate(self, method: AuthMethod = AuthMethod.API_KEY) -> bool:
        """Authenticate with OpenRouter"""
        if method == AuthMethod.API_KEY:
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
                return True
            except Exception as e:
                print(f"❌ {self.model_name}: Auth failed - {e}")
                return False

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

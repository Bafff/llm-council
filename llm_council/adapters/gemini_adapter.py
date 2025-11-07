"""Gemini adapter - FREE API from Google"""

import os
import time
from typing import Optional
from google import genai

from .base import BaseLLMAdapter, LLMResponse, AuthMethod


class GeminiAdapter(BaseLLMAdapter):
    """Adapter for Gemini (FREE 60 req/min!)"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.client = None
        self.api_key: Optional[str] = None
        # Use latest Gemini 2.5 Flash (newest model as of 2025)
        self.model_id = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')

    def authenticate(self, method: AuthMethod = AuthMethod.API_KEY) -> bool:
        """Authenticate with Gemini using new SDK"""
        if method == AuthMethod.API_KEY:
            # Try environment variable
            self.api_key = os.getenv('GOOGLE_API_KEY')

            if not self.api_key:
                print(f"⚠️  {self.model_name}: No API key found")
                print("   Get FREE key at: https://ai.google.dev/")
                return False

            try:
                # Use new Gemini SDK (from google import genai)
                self.client = genai.Client(api_key=self.api_key)
                return True
            except Exception as e:
                print(f"❌ {self.model_name}: Auth failed - {e}")
                return False

        return False

    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Query Gemini using new SDK"""
        if not self.client:
            if not self.authenticate():
                return LLMResponse(
                    model_name=self.model_name,
                    content="",
                    error="Authentication failed"
                )

        start_time = time.time()

        try:
            # New Gemini SDK: client.models.generate_content()
            import asyncio
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=prompt
            )

            latency = (time.time() - start_time) * 1000

            # Extract text from response
            content = response.text if hasattr(response, 'text') else str(response)

            # Get token usage if available
            tokens = getattr(response, 'usage_metadata', None)
            token_count = None
            if tokens:
                token_count = getattr(tokens, 'total_token_count', None)

            return LLMResponse(
                model_name=self.model_name,
                content=content,
                confidence=0.85,
                tokens_used=token_count,
                latency_ms=latency,
                raw_response={'response': str(response)}
            )

        except Exception as e:
            return LLMResponse(
                model_name=self.model_name,
                content="",
                error=f"Query failed: {str(e)}"
            )

"""Gemini adapter - FREE API from Google"""

import os
import time
from typing import Optional
import google.generativeai as genai

from .base import BaseLLMAdapter, LLMResponse, AuthMethod


class GeminiAdapter(BaseLLMAdapter):
    """Adapter for Gemini (FREE 60 req/min!)"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.client = None
        self.api_key: Optional[str] = None
        self.model_id = "gemini-2.0-flash-exp"  # Latest free model

    def authenticate(self, method: AuthMethod = AuthMethod.API_KEY) -> bool:
        """Authenticate with Gemini"""
        if method == AuthMethod.API_KEY:
            # Try environment variable
            self.api_key = os.getenv('GOOGLE_API_KEY')

            if not self.api_key:
                print(f"⚠️  {self.model_name}: No API key found")
                print("   Get FREE key at: https://ai.google.dev/")
                return False

            try:
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model_id)
                return True
            except Exception as e:
                print(f"❌ {self.model_name}: Auth failed - {e}")
                return False

        return False

    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Query Gemini"""
        if not self.client:
            if not self.authenticate():
                return LLMResponse(
                    model_name=self.model_name,
                    content="",
                    error="Authentication failed"
                )

        start_time = time.time()

        try:
            # Gemini's generate_content is sync, wrap in async
            import asyncio
            response = await asyncio.to_thread(
                self.client.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 4096),
                )
            )

            latency = (time.time() - start_time) * 1000

            # Extract text from response
            content = response.text if hasattr(response, 'text') else str(response)

            # Estimate tokens (Gemini doesn't always return exact count)
            tokens = getattr(response, 'usage_metadata', None)
            token_count = None
            if tokens:
                token_count = tokens.prompt_token_count + tokens.candidates_token_count

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

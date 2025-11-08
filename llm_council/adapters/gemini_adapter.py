"""Gemini adapter - FREE API from Google"""

import os
import time
from typing import Optional
import httpx

from .base import BaseLLMAdapter, LLMResponse, AuthMethod


class GeminiAdapter(BaseLLMAdapter):
    """Adapter for Gemini (FREE 60 req/min!)"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.api_key: Optional[str] = None
        # Use latest Gemini 2.5 Flash (newest model as of 2025)
        self.model_id = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def authenticate(self, method: AuthMethod = AuthMethod.API_KEY) -> bool:
        """Authenticate with Gemini using REST API"""
        if method == AuthMethod.API_KEY:
            # Try environment variable
            self.api_key = os.getenv('GOOGLE_API_KEY')

            if not self.api_key:
                print(f"⚠️  {self.model_name}: No API key found")
                print("   Get FREE key at: https://ai.google.dev/")
                return False

            return True

        return False

    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Query Gemini using direct REST API"""
        if not self.api_key:
            if not self.authenticate():
                return LLMResponse(
                    model_name=self.model_name,
                    content="",
                    error="Authentication failed"
                )

        start_time = time.time()

        try:
            # Direct REST API call (works where SDK fails)
            url = f"{self.base_url}/{self.model_id}:generateContent"

            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    headers={
                        'Content-Type': 'application/json',
                        'x-goog-api-key': self.api_key
                    },
                    json=payload
                )
                response.raise_for_status()
                data = response.json()

            latency = (time.time() - start_time) * 1000

            # Extract text from response
            content = data['candidates'][0]['content']['parts'][0]['text']

            # Get token usage if available
            token_count = None
            if 'usageMetadata' in data:
                usage = data['usageMetadata']
                token_count = usage.get('totalTokenCount')

            return LLMResponse(
                model_name=self.model_name,
                content=content,
                confidence=0.85,
                tokens_used=token_count,
                latency_ms=latency,
                raw_response=data
            )

        except httpx.HTTPStatusError as e:
            return LLMResponse(
                model_name=self.model_name,
                content="",
                error=f"HTTP {e.response.status_code}: {e.response.text[:200]}"
            )
        except Exception as e:
            return LLMResponse(
                model_name=self.model_name,
                content="",
                error=f"Query failed: {str(e)}"
            )

"""Gemini adapter - FREE API from Google"""

import os
import time
from typing import Optional
import httpx

from .base import BaseLLMAdapter, LLMResponse, AuthMethod
from ..auth import CLISessionManager, CLIProvider


class GeminiAdapter(BaseLLMAdapter):
    """Adapter for Gemini (FREE 60 req/min!)"""

    def __init__(self, config: dict):
        super().__init__(config)
        self.api_key: Optional[str] = None
        self.bearer_token: Optional[str] = None  # For gcloud OAuth tokens
        # Use latest Gemini 2.5 Flash (newest model as of 2025)
        self.model_id = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"
        self.cli_session_manager = CLISessionManager()
        self.use_cli_auth = config.get('use_cli_auth', True)  # Default: try CLI first

    def authenticate(self, method: AuthMethod = AuthMethod.CLI_SESSION) -> bool:
        """
        Authenticate with Gemini using CLI session or API key.

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
        """Authenticate using Gemini/gcloud CLI session"""
        try:
            # Try Gemini CLI
            session = self.cli_session_manager.get_session(CLIProvider.GEMINI)
            if session.is_authenticated and session.api_key:
                self.api_key = session.api_key
                self.auth_method_used = "CLI Session"
                self.auth_source = "Gemini CLI"
                print(f"✅ {self.model_name}: Authenticated via Gemini CLI")
                return True

            # Try Google Cloud CLI (gcloud)
            session = self.cli_session_manager.get_session(CLIProvider.GOOGLE_AI)
            if session.is_authenticated and (session.token or session.api_key):
                # gcloud returns bearer tokens (OAuth), not API keys
                if session.token:
                    self.bearer_token = session.token
                    self.auth_method_used = "CLI Session"
                    self.auth_source = "gcloud CLI (OAuth Bearer Token)"
                    print(f"✅ {self.model_name}: Authenticated via gcloud CLI (OAuth)")
                else:
                    self.api_key = session.api_key
                    self.auth_method_used = "CLI Session"
                    self.auth_source = "gcloud CLI"
                    print(f"✅ {self.model_name}: Authenticated via gcloud CLI")
                return True

        except Exception as e:
            print(f"⚠️  {self.model_name}: CLI auth failed - {e}")

        return False

    def _authenticate_via_api_key(self) -> bool:
        """Authenticate using API key from environment"""
        self.api_key = os.getenv('GOOGLE_API_KEY')

        if not self.api_key:
            print(f"⚠️  {self.model_name}: No API key found")
            print("   Get FREE key at: https://ai.google.dev/")
            return False

        self.auth_method_used = "API Key"
        self.auth_source = "GOOGLE_API_KEY env var"
        print(f"✅ {self.model_name}: Authenticated via API key")
        return True

    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """Query Gemini using direct REST API"""
        if not self.api_key and not self.bearer_token:
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

            # Build headers based on auth type
            headers = {'Content-Type': 'application/json'}

            if self.bearer_token:
                # gcloud OAuth token - use Authorization: Bearer header
                headers['Authorization'] = f'Bearer {self.bearer_token}'
            elif self.api_key:
                # API key - use x-goog-api-key header
                headers['x-goog-api-key'] = self.api_key
            else:
                return LLMResponse(
                    model_name=self.model_name,
                    content="",
                    error="No authentication credentials available"
                )

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
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
                raw_response=data,
                auth_method=self.auth_method_used,
                auth_source=self.auth_source
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

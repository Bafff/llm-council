"""Base adapter interface for LLM providers"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum


class AuthMethod(Enum):
    """Authentication methods"""
    API_KEY = "api_key"
    BROWSER_COOKIES = "browser_cookies"
    OAUTH = "oauth"
    CLAUDE_CODE_SESSION = "claude_code_session"


@dataclass
class LLMResponse:
    """Standardized response from any LLM"""
    model_name: str
    content: str
    confidence: float = 0.85  # Default confidence
    tokens_used: Optional[int] = None
    latency_ms: Optional[float] = None
    raw_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None


class BaseLLMAdapter(ABC):
    """Base class for all LLM adapters"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get('display_name', 'Unknown Model')
        self.weight = config.get('weight', 1.0)
        self.enabled = config.get('enabled', True)

    @abstractmethod
    async def query(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Send a query to the LLM and get a response.

        Args:
            prompt: The user's question/prompt
            **kwargs: Additional provider-specific parameters

        Returns:
            LLMResponse with the model's answer
        """
        pass

    @abstractmethod
    def authenticate(self, method: AuthMethod = AuthMethod.API_KEY) -> bool:
        """
        Authenticate with the LLM provider.

        Args:
            method: Authentication method to use

        Returns:
            True if authentication successful, False otherwise
        """
        pass

    def is_available(self) -> bool:
        """Check if this adapter is available and ready"""
        return self.enabled and self.authenticate()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(model={self.model_name}, weight={self.weight})>"

"""Pytest configuration and fixtures for LLM Council tests"""

import pytest

from llm_council.adapters.base import LLMResponse


@pytest.fixture
def mock_config():
    """Mock configuration for testing"""
    return {
        'models': {
            'claude': {
                'enabled': True,
                'adapter': 'claude',
                'display_name': 'Claude Sonnet 4.5',
                'weight': 1.2
            },
            'gemini': {
                'enabled': True,
                'adapter': 'gemini',
                'display_name': 'Gemini 1.5 Flash',
                'weight': 1.0
            },
            'gpt4': {
                'enabled': True,
                'adapter': 'openrouter',
                'display_name': 'GPT-4 Turbo',
                'weight': 1.1
            }
        },
        'synthesis': {
            'method': 'weighted_consensus',
            'strong_consensus': 0.8,
            'weak_consensus': 0.6,
            'enable_meta_analysis': True
        }
    }


@pytest.fixture
def mock_llm_response_success():
    """Mock successful LLM response"""
    return LLMResponse(
        model_name="Test Model",
        content="This is a test response",
        confidence=0.9,
        tokens_used=100,
        latency_ms=500.0
    )


@pytest.fixture
def mock_llm_response_error():
    """Mock failed LLM response"""
    return LLMResponse(
        model_name="Test Model",
        content="",
        error="Connection timeout"
    )


@pytest.fixture
def mock_responses_agreement():
    """Mock responses where models agree (strong consensus)"""
    return [
        {
            'model': 'claude',
            'display_name': 'Claude Sonnet 4.5',
            'weight': 1.2,
            'response': LLMResponse(
                model_name="Claude Sonnet 4.5",
                content="Python is better for data science due to libraries like NumPy and Pandas.",
                confidence=0.9,
                tokens_used=50
            )
        },
        {
            'model': 'gemini',
            'display_name': 'Gemini 1.5 Flash',
            'weight': 1.0,
            'response': LLMResponse(
                model_name="Gemini 1.5 Flash",
                content="Python is preferred for data science because of its extensive ecosystem.",
                confidence=0.85,
                tokens_used=48
            )
        },
        {
            'model': 'gpt4',
            'display_name': 'GPT-4 Turbo',
            'weight': 1.1,
            'response': LLMResponse(
                model_name="GPT-4 Turbo",
                content="Python is the best choice for data science due to mature libraries.",
                confidence=0.88,
                tokens_used=52
            )
        }
    ]


@pytest.fixture
def mock_responses_disagreement():
    """Mock responses where models disagree (conflicted consensus)"""
    return [
        {
            'model': 'claude',
            'display_name': 'Claude Sonnet 4.5',
            'weight': 1.2,
            'response': LLMResponse(
                model_name="Claude Sonnet 4.5",
                content="JavaScript is better for web development due to full-stack capability.",
                confidence=0.8,
                tokens_used=45
            )
        },
        {
            'model': 'gemini',
            'display_name': 'Gemini 1.5 Flash',
            'weight': 1.0,
            'response': LLMResponse(
                model_name="Gemini 1.5 Flash",
                content="Python is better for web backends due to simplicity and Django.",
                confidence=0.75,
                tokens_used=42
            )
        },
        {
            'model': 'gpt4',
            'display_name': 'GPT-4 Turbo',
            'weight': 1.1,
            'response': LLMResponse(
                model_name="GPT-4 Turbo",
                content="Go is better for web services due to performance and concurrency.",
                confidence=0.82,
                tokens_used=48
            )
        }
    ]


@pytest.fixture
def mock_responses_partial():
    """Mock responses where some models fail"""
    return [
        {
            'model': 'claude',
            'display_name': 'Claude Sonnet 4.5',
            'weight': 1.2,
            'response': LLMResponse(
                model_name="Claude Sonnet 4.5",
                content="Docker is a containerization platform.",
                confidence=0.95,
                tokens_used=30
            )
        },
        {
            'model': 'gemini',
            'display_name': 'Gemini 1.5 Flash',
            'weight': 1.0,
            'response': LLMResponse(
                model_name="Gemini 1.5 Flash",
                content="",
                error="API rate limit exceeded"
            )
        },
        {
            'model': 'gpt4',
            'display_name': 'GPT-4 Turbo',
            'weight': 1.1,
            'response': LLMResponse(
                model_name="GPT-4 Turbo",
                content="Docker is a tool for running applications in isolated containers.",
                confidence=0.90,
                tokens_used=35
            )
        }
    ]


@pytest.fixture
def simple_prompt():
    """Simple test prompt"""
    return "What is 2+2?"


@pytest.fixture
def complex_prompt():
    """Complex test prompt"""
    return "Compare microservices vs monolithic architecture for a startup with 5 developers."

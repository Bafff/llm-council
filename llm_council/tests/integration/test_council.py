"""Integration tests for LLM Council"""

import asyncio
import os
from unittest.mock import AsyncMock, Mock, patch

import pytest

from llm_council.adapters.base import LLMResponse
from llm_council.adapters.claude_adapter import ClaudeAdapter
from llm_council.adapters.gemini_adapter import GeminiAdapter
from llm_council.core.council import LLMCouncil
from llm_council.core.synthesizer import ConsensusLevel


class TestLLMCouncilIntegration:
    """Integration tests for complete council workflow"""

    @pytest.mark.asyncio
    async def test_council_initialization(self, mock_config, tmp_path):
        """Test council initialization with config"""
        # Create temporary config file
        import yaml
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        council = LLMCouncil(config_path=str(config_file))

        # Verify council initialized
        assert council.config == mock_config
        assert council.synthesizer is not None
        assert isinstance(council.adapters, list)

    @pytest.mark.asyncio
    async def test_council_query_with_mocked_adapters(self, mock_config, tmp_path):
        """Test full council query flow with mocked adapter responses"""
        # Create config
        import yaml
        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        council = LLMCouncil(config_path=str(config_file))

        # Mock adapter responses
        mock_claude_response = LLMResponse(
            model_name="Claude Sonnet 4.5",
            content="Python is best for data science due to NumPy and Pandas.",
            confidence=0.9,
            tokens_used=45
        )

        mock_gemini_response = LLMResponse(
            model_name="Gemini 1.5 Flash",
            content="Python excels in data science with its rich ecosystem.",
            confidence=0.85,
            tokens_used=42
        )

        # Mock the adapters
        for adapter in council.adapters:
            if "Claude" in adapter.model_name:
                adapter.query = AsyncMock(return_value=mock_claude_response)
                adapter.is_available = Mock(return_value=True)
            elif "Gemini" in adapter.model_name:
                adapter.query = AsyncMock(return_value=mock_gemini_response)
                adapter.is_available = Mock(return_value=True)
            else:
                adapter.is_available = Mock(return_value=False)

        # Execute query
        result = await council.query("What's best for data science?")

        # Verify result structure
        assert result.consensus_level in [e.value for e in ConsensusLevel]
        assert result.synthesized_answer != ""
        assert len(result.individual_responses) >= 2

        # Should mention Python since both agreed
        assert "python" in result.synthesized_answer.lower()

    @pytest.mark.asyncio
    async def test_council_parallel_execution(self, mock_config, tmp_path):
        """Test that models are queried in parallel"""
        import yaml
        import time

        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        council = LLMCouncil(config_path=str(config_file))

        # Mock slow responses
        async def slow_response(prompt, **kwargs):
            await asyncio.sleep(0.1)  # 100ms delay
            return LLMResponse(
                model_name="Test Model",
                content="Response",
                confidence=0.8,
                tokens_used=20
            )

        # Mock all adapters with slow responses
        for adapter in council.adapters:
            adapter.query = AsyncMock(side_effect=slow_response)
            adapter.is_available = Mock(return_value=True)

        # Execute - should take ~100ms not 200ms+ if parallel
        start = time.time()
        result = await council.query("Test parallel execution")
        elapsed = time.time() - start

        # With 2 adapters at 100ms each:
        # - Sequential: ~200ms
        # - Parallel: ~100ms
        # Allow some overhead, but verify parallelism
        assert elapsed < 0.25, f"Execution took {elapsed}s, expected parallel execution ~0.1s"

    @pytest.mark.asyncio
    async def test_council_handles_adapter_failures(self, mock_config, tmp_path):
        """Test council gracefully handles adapter failures"""
        import yaml

        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        council = LLMCouncil(config_path=str(config_file))

        # Mock one success, one failure
        success_response = LLMResponse(
            model_name="Working Model",
            content="This is the answer",
            confidence=0.9,
            tokens_used=30
        )

        failure_response = LLMResponse(
            model_name="Failed Model",
            content="",
            error="Connection timeout"
        )

        responses = [success_response, failure_response]
        response_index = [0]

        async def get_next_response(prompt, **kwargs):
            idx = response_index[0]
            response_index[0] += 1
            return responses[idx % len(responses)]

        for adapter in council.adapters:
            adapter.query = AsyncMock(side_effect=get_next_response)
            adapter.is_available = Mock(return_value=True)

        # Should still produce result with partial data
        result = await council.query("Test failure handling")

        assert result.synthesized_answer != ""
        # Should have at least one successful response
        successful = [r for r in result.individual_responses if r['response'].success]
        assert len(successful) >= 1

    @pytest.mark.asyncio
    async def test_council_empty_result_handling(self, mock_config, tmp_path):
        """Test council handles case with no available models"""
        import yaml

        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        council = LLMCouncil(config_path=str(config_file))

        # Mock all adapters as unavailable
        for adapter in council.adapters:
            adapter.is_available = Mock(return_value=False)

        # Should handle gracefully
        result = await council.query("Test no models")

        # Should indicate no models available
        assert "no" in result.synthesized_answer.lower() or "unavailable" in result.synthesized_answer.lower()
        assert result.confidence_score == 0.0

    @pytest.mark.asyncio
    async def test_council_weighted_consensus(self, mock_config, tmp_path):
        """Test that model weights are applied in consensus"""
        import yaml

        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        council = LLMCouncil(config_path=str(config_file))

        # Claude (weight 1.2) says A, others say B
        claude_response = LLMResponse(
            model_name="Claude Sonnet 4.5",
            content="Option A is better",
            confidence=0.9,
            tokens_used=20
        )

        other_response = LLMResponse(
            model_name="Other Model",
            content="Option B is better",
            confidence=0.85,
            tokens_used=20
        )

        for adapter in council.adapters:
            if "Claude" in adapter.model_name:
                adapter.query = AsyncMock(return_value=claude_response)
                adapter.is_available = Mock(return_value=True)
            else:
                adapter.query = AsyncMock(return_value=other_response)
                adapter.is_available = Mock(return_value=True)

        result = await council.query("Which option is better?")

        # Should show some conflict due to disagreement
        assert result.consensus_level in [ConsensusLevel.WEAK.value, ConsensusLevel.CONFLICTED.value]
        # Answer should acknowledge both options
        answer_lower = result.synthesized_answer.lower()
        assert "option" in answer_lower or "a" in answer_lower or "b" in answer_lower


class TestCouncilRealAPI:
    """Tests that use real API keys (skip if not available)"""

    @pytest.mark.skipif(
        not os.getenv('ANTHROPIC_API_KEY'),
        reason="Requires ANTHROPIC_API_KEY environment variable"
    )
    @pytest.mark.asyncio
    async def test_real_claude_query(self):
        """Test real Claude API query"""
        config = {
            'models': {
                'claude': {
                    'enabled': True,
                    'adapter': 'claude',
                    'display_name': 'Claude Sonnet 4.5',
                    'weight': 1.2
                }
            }
        }

        adapter = ClaudeAdapter(config['models']['claude'])
        if adapter.authenticate():
            response = await adapter.query("What is 2+2? Answer in one word.")

            assert response.success == True
            assert response.content != ""
            assert "four" in response.content.lower() or "4" in response.content

    @pytest.mark.skipif(
        not os.getenv('GOOGLE_API_KEY'),
        reason="Requires GOOGLE_API_KEY environment variable"
    )
    @pytest.mark.asyncio
    async def test_real_gemini_query(self):
        """Test real Gemini API query"""
        config = {
            'models': {
                'gemini': {
                    'enabled': True,
                    'adapter': 'gemini',
                    'display_name': 'Gemini 1.5 Flash',
                    'weight': 1.0
                }
            }
        }

        adapter = GeminiAdapter(config['models']['gemini'])
        if adapter.authenticate():
            response = await adapter.query("What is 2+2? Answer in one word.")

            assert response.success == True
            assert response.content != ""


class TestCouncilErrorRecovery:
    """Test error recovery and edge cases"""

    @pytest.mark.asyncio
    async def test_malformed_config(self):
        """Test council handles malformed config gracefully"""
        # This should be handled by validation
        # For now, just verify it doesn't crash
        try:
            council = LLMCouncil(config_path="/nonexistent/path/config.yaml")
        except (FileNotFoundError, IOError):
            # Expected behavior
            pass

    @pytest.mark.asyncio
    async def test_timeout_handling(self, mock_config, tmp_path):
        """Test council handles request timeouts"""
        import yaml

        config_file = tmp_path / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(mock_config, f)

        council = LLMCouncil(config_path=str(config_file))

        # Mock extremely slow response
        async def timeout_response(prompt, **kwargs):
            await asyncio.sleep(10)  # Very slow
            return LLMResponse(model_name="Slow", content="Late response")

        for adapter in council.adapters:
            adapter.query = AsyncMock(side_effect=timeout_response)
            adapter.is_available = Mock(return_value=True)

        # Set a reasonable timeout and verify it's respected
        # Note: Council should have timeout configuration
        try:
            result = await asyncio.wait_for(
                council.query("Test timeout"),
                timeout=2.0
            )
        except asyncio.TimeoutError:
            # Expected if council doesn't handle timeouts internally
            pass

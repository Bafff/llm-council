"""Unit tests for ConsensusSynthesizer"""

import pytest
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.synthesizer import ConsensusSynthesizer, ConsensusLevel
from adapters.base import LLMResponse


class TestConsensusSynthesizer:
    """Test consensus synthesis logic"""

    def test_initialization(self, mock_config):
        """Test synthesizer initialization"""
        synthesizer = ConsensusSynthesizer(mock_config)
        assert synthesizer.config == mock_config
        assert synthesizer.strong_threshold == 0.8
        assert synthesizer.weak_threshold == 0.6

    def test_strong_consensus(self, mock_config, mock_responses_agreement):
        """Test strong consensus when all models agree"""
        synthesizer = ConsensusSynthesizer(mock_config)
        result = synthesizer.synthesize(mock_responses_agreement, "Which language is better for data science?")

        # Should detect strong consensus
        assert result.consensus_level == ConsensusLevel.STRONG
        assert result.confidence_score >= 0.8

        # Should have all responses
        assert len(result.individual_responses) == 3

        # Should find agreements
        assert len(result.agreements) > 0
        assert any("Python" in str(agreement) for agreement in result.agreements)

        # Synthesized answer should mention Python
        assert "Python" in result.synthesized_answer or "python" in result.synthesized_answer.lower()

    def test_conflicted_consensus(self, mock_config, mock_responses_disagreement):
        """Test conflicted consensus when models disagree"""
        synthesizer = ConsensusSynthesizer(mock_config)
        result = synthesizer.synthesize(mock_responses_disagreement, "Which language for web backends?")

        # Should detect conflict
        assert result.consensus_level in [ConsensusLevel.WEAK, ConsensusLevel.CONFLICTED]
        assert result.confidence_score < 0.8

        # Should have disagreements
        assert len(result.disagreements) > 0

        # Should mention multiple languages
        answer_lower = result.synthesized_answer.lower()
        mentioned_languages = sum([
            "javascript" in answer_lower,
            "python" in answer_lower,
            "go" in answer_lower
        ])
        assert mentioned_languages >= 2

    def test_partial_responses(self, mock_config, mock_responses_partial):
        """Test handling of partial responses (some models failed)"""
        synthesizer = ConsensusSynthesizer(mock_config)
        result = synthesizer.synthesize(mock_responses_partial, "What is Docker?")

        # Should still work with 2/3 models
        assert result.synthesized_answer != ""

        # Should have 2 successful responses
        successful = [r for r in result.individual_responses if r['response'].success]
        assert len(successful) == 2

        # Should mention Docker
        assert "Docker" in result.synthesized_answer or "docker" in result.synthesized_answer.lower()

    def test_empty_responses(self, mock_config):
        """Test handling of all failed responses"""
        synthesizer = ConsensusSynthesizer(mock_config)

        empty_responses = [
            {
                'model': 'claude',
                'display_name': 'Claude',
                'weight': 1.2,
                'response': LLMResponse(model_name="Claude", content="", error="Failed")
            },
            {
                'model': 'gemini',
                'display_name': 'Gemini',
                'weight': 1.0,
                'response': LLMResponse(model_name="Gemini", content="", error="Failed")
            }
        ]

        result = synthesizer.synthesize(empty_responses, "Test question")

        # Should handle gracefully
        assert result.consensus_level == ConsensusLevel.CONFLICTED
        assert result.confidence_score == 0.0
        assert "no successful responses" in result.synthesized_answer.lower() or "failed" in result.synthesized_answer.lower()

    def test_weighted_voting(self, mock_config):
        """Test that weights are properly applied"""
        synthesizer = ConsensusSynthesizer(mock_config)

        # Claude (weight 1.2) says A, others (weight 1.0 each) say B
        responses = [
            {
                'model': 'claude',
                'display_name': 'Claude',
                'weight': 1.2,
                'response': LLMResponse(
                    model_name="Claude",
                    content="The answer is A because of reason X.",
                    confidence=0.9
                )
            },
            {
                'model': 'gemini',
                'display_name': 'Gemini',
                'weight': 1.0,
                'response': LLMResponse(
                    model_name="Gemini",
                    content="The answer is B due to reason Y.",
                    confidence=0.85
                )
            },
            {
                'model': 'gpt4',
                'display_name': 'GPT-4',
                'weight': 1.0,
                'response': LLMResponse(
                    model_name="GPT-4",
                    content="I think B is correct for reason Z.",
                    confidence=0.88
                )
            }
        ]

        result = synthesizer.synthesize(responses, "Is the answer A or B?")

        # With weights: Claude (1.2 * 0.9 = 1.08) vs Gemini+GPT4 (1.0*0.85 + 1.0*0.88 = 1.73)
        # B should win but it should be conflicted
        assert result.consensus_level in [ConsensusLevel.WEAK, ConsensusLevel.CONFLICTED]

    def test_confidence_calculation(self, mock_config, mock_responses_agreement):
        """Test confidence score calculation"""
        synthesizer = ConsensusSynthesizer(mock_config)
        result = synthesizer.synthesize(mock_responses_agreement, "Test")

        # Confidence should be between 0 and 1
        assert 0.0 <= result.confidence_score <= 1.0

        # Strong consensus should have high confidence
        if result.consensus_level == ConsensusLevel.STRONG:
            assert result.confidence_score >= 0.8

    def test_agreement_detection(self, mock_config, mock_responses_agreement):
        """Test detection of agreement points"""
        synthesizer = ConsensusSynthesizer(mock_config)
        result = synthesizer.synthesize(mock_responses_agreement, "Data science language")

        # Should detect agreement on Python
        agreements_text = " ".join(result.agreements)
        assert "python" in agreements_text.lower()

    def test_disagreement_detection(self, mock_config, mock_responses_disagreement):
        """Test detection of disagreement points"""
        synthesizer = ConsensusSynthesizer(mock_config)
        result = synthesizer.synthesize(mock_responses_disagreement, "Web backend language")

        # Should detect disagreements
        assert len(result.disagreements) > 0

        # Should capture different opinions
        disagreements_text = " ".join(result.disagreements).lower()
        mentioned_count = sum([
            "javascript" in disagreements_text,
            "python" in disagreements_text,
            "go" in disagreements_text
        ])
        assert mentioned_count >= 2


class TestConsensusLevels:
    """Test consensus level enum and thresholds"""

    def test_consensus_level_enum(self):
        """Test ConsensusLevel enum values"""
        assert ConsensusLevel.STRONG == "strong"
        assert ConsensusLevel.MODERATE == "moderate"
        assert ConsensusLevel.WEAK == "weak"
        assert ConsensusLevel.CONFLICTED == "conflicted"

    def test_threshold_boundaries(self, mock_config):
        """Test consensus level boundaries"""
        synthesizer = ConsensusSynthesizer(mock_config)

        # Test boundary conditions
        assert synthesizer.strong_threshold == 0.8  # 80%
        assert synthesizer.weak_threshold == 0.6    # 60%

        # Verify thresholds are in correct order
        assert synthesizer.weak_threshold < synthesizer.strong_threshold

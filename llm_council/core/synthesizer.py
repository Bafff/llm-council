"""Consensus Synthesizer - inspired by claude-code-council"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from enum import Enum
import re


class ConsensusLevel(Enum):
    """Level of consensus between models"""
    STRONG = "strong"       # 80%+ agreement
    MODERATE = "moderate"   # 60-80% agreement
    WEAK = "weak"           # 40-60% agreement
    CONFLICTED = "conflicted"  # <40% agreement


@dataclass
class SynthesisResult:
    """Result of consensus synthesis"""
    consensus_level: ConsensusLevel
    confidence_score: float  # 0.0 - 1.0
    synthesized_answer: str
    individual_responses: List[Dict]
    agreements: List[str]
    disagreements: List[str]
    meta_analysis: Optional[str] = None  # Analysis of why models disagree


class ConsensusSynthesizer:
    """
    Synthesize consensus from multiple LLM responses.

    Inspired by claude-code-council's weighted voting system.
    """

    def __init__(self, config: dict):
        self.config = config
        self.synthesis_method = config.get('synthesis', {}).get('method', 'weighted_consensus')
        self.strong_threshold = config.get('synthesis', {}).get('strong_consensus', 0.8)
        self.weak_threshold = config.get('synthesis', {}).get('weak_consensus', 0.6)

    def synthesize(self, responses: List[Dict], prompt: str) -> SynthesisResult:
        """
        Main synthesis method.

        Args:
            responses: List of {adapter, response} dicts
            prompt: Original user prompt

        Returns:
            SynthesisResult with consensus analysis
        """
        # Filter successful responses
        valid_responses = [
            r for r in responses
            if r['response'].success and r['response'].content
        ]

        if not valid_responses:
            return self._error_result("No valid responses received")

        if len(valid_responses) == 1:
            return self._single_response_result(valid_responses[0])

        # Analyze agreements and disagreements
        agreements, disagreements = self._find_consensus_points(valid_responses)

        # Calculate consensus level
        consensus_level, confidence = self._calculate_consensus(
            agreements, disagreements, valid_responses
        )

        # Generate synthesized answer
        synthesized = self._generate_synthesis(
            valid_responses, agreements, disagreements, consensus_level
        )

        # Meta-analysis if there are significant disagreements
        meta_analysis = None
        if len(disagreements) > 0 and self.config.get('synthesis', {}).get('enable_meta_analysis', True):
            meta_analysis = self._generate_meta_analysis(
                valid_responses, disagreements, prompt
            )

        return SynthesisResult(
            consensus_level=consensus_level,
            confidence_score=confidence,
            synthesized_answer=synthesized,
            individual_responses=[
                {
                    'model': r['adapter'].model_name,
                    'content': r['response'].content,
                    'confidence': r['response'].confidence,
                    'weight': r['adapter'].weight,
                    'auth_method': r['response'].auth_method,
                    'auth_source': r['response'].auth_source
                }
                for r in valid_responses
            ],
            agreements=agreements,
            disagreements=disagreements,
            meta_analysis=meta_analysis
        )

    def _find_consensus_points(self, responses: List[Dict]) -> Tuple[List[str], List[str]]:
        """Find what models agree and disagree on"""

        # Extract key statements from each response
        all_statements = []
        for r in responses:
            statements = self._extract_key_statements(r['response'].content)
            all_statements.append({
                'model': r['adapter'].model_name,
                'statements': statements,
                'weight': r['adapter'].weight
            })

        # Find common themes (agreements)
        agreements = self._find_common_themes(all_statements)

        # Find contradictions (disagreements)
        disagreements = self._find_contradictions(all_statements)

        return agreements, disagreements

    def _extract_key_statements(self, content: str) -> List[str]:
        """Extract key statements from response"""
        # Split by sentences
        sentences = re.split(r'[.!?]+', content)

        # Filter out short sentences and clean
        statements = [
            s.strip()
            for s in sentences
            if len(s.strip()) > 20 and not s.strip().startswith(('However', 'But', 'Although'))
        ]

        return statements[:10]  # Top 10 key statements

    def _find_common_themes(self, all_statements: List[Dict]) -> List[str]:
        """Find themes that appear in multiple responses"""
        agreements = []

        # Simple keyword matching (can be improved with embeddings)
        all_words = {}
        for model_data in all_statements:
            for statement in model_data['statements']:
                # Extract significant words (>4 chars)
                words = [w.lower() for w in re.findall(r'\b\w{5,}\b', statement)]
                for word in words:
                    if word not in all_words:
                        all_words[word] = []
                    all_words[word].append({
                        'model': model_data['model'],
                        'statement': statement
                    })

        # Find words mentioned by multiple models
        for word, mentions in all_words.items():
            unique_models = set(m['model'] for m in mentions)
            if len(unique_models) >= len(all_statements) * 0.6:  # 60% of models
                # Find the best statement containing this word
                statement = mentions[0]['statement']
                agreements.append(f"Multiple models agree: {statement}")

        return agreements[:5]  # Top 5 agreements

    def _find_contradictions(self, all_statements: List[Dict]) -> List[str]:
        """Find contradictory statements"""
        disagreements = []

        # Look for opposite keywords
        opposites = [
            ('yes', 'no'),
            ('true', 'false'),
            ('correct', 'incorrect'),
            ('should', 'should not'),
            ('can', 'cannot'),
            ('will', 'will not'),
            ('always', 'never'),
        ]

        for model1 in all_statements:
            for model2 in all_statements:
                if model1['model'] >= model2['model']:  # Avoid duplicates
                    continue

                for stmt1 in model1['statements']:
                    for stmt2 in model2['statements']:
                        # Check for opposite keywords
                        for pos, neg in opposites:
                            if pos in stmt1.lower() and neg in stmt2.lower():
                                disagreements.append(
                                    f"{model1['model']} says: {stmt1[:100]}...\n"
                                    f"  vs {model2['model']} says: {stmt2[:100]}..."
                                )
                                break

        return disagreements[:5]  # Top 5 disagreements

    def _calculate_consensus(
        self,
        agreements: List[str],
        disagreements: List[str],
        responses: List[Dict]
    ) -> Tuple[ConsensusLevel, float]:
        """Calculate consensus level and confidence"""

        # Weighted consensus score
        total_weight = sum(r['adapter'].weight for r in responses)
        agreement_weight = len(agreements) / max(len(agreements) + len(disagreements), 1)

        # Incorporate model confidence
        avg_confidence = sum(
            r['response'].confidence * r['adapter'].weight
            for r in responses
        ) / total_weight

        # Final confidence score
        confidence = (agreement_weight * 0.6 + avg_confidence * 0.4)

        # Determine consensus level
        if confidence >= self.strong_threshold:
            return ConsensusLevel.STRONG, confidence
        elif confidence >= self.weak_threshold:
            return ConsensusLevel.MODERATE, confidence
        elif confidence >= 0.4:
            return ConsensusLevel.WEAK, confidence
        else:
            return ConsensusLevel.CONFLICTED, confidence

    def _generate_synthesis(
        self,
        responses: List[Dict],
        agreements: List[str],
        disagreements: List[str],
        consensus_level: ConsensusLevel
    ) -> str:
        """Generate final synthesized answer"""

        synthesis = []

        # Header based on consensus
        if consensus_level == ConsensusLevel.STRONG:
            synthesis.append("✅ **Strong Consensus** - All models largely agree:\n")
        elif consensus_level == ConsensusLevel.MODERATE:
            synthesis.append("⚠️  **Moderate Consensus** - Models mostly agree with some variations:\n")
        elif consensus_level == ConsensusLevel.WEAK:
            synthesis.append("❓ **Weak Consensus** - Significant differences in responses:\n")
        else:
            synthesis.append("⚡ **Conflicted** - Models have contradictory answers:\n")

        # Common points
        if agreements:
            synthesis.append("\n**Common Points:**")
            for i, agreement in enumerate(agreements, 1):
                synthesis.append(f"{i}. {agreement}")

        # Take the highest-weighted response as primary
        primary_response = max(
            responses,
            key=lambda r: r['adapter'].weight * r['response'].confidence
        )

        synthesis.append(f"\n**Synthesized Answer (based on {primary_response['adapter'].model_name}):**")
        synthesis.append(primary_response['response'].content)

        # Mention disagreements
        if disagreements:
            synthesis.append("\n**⚠️  Note: Some Disagreements Found:**")
            for disagreement in disagreements[:3]:
                synthesis.append(f"- {disagreement}")

        return "\n".join(synthesis)

    def _generate_meta_analysis(
        self,
        responses: List[Dict],
        disagreements: List[str],
        original_prompt: str
    ) -> str:
        """Generate analysis of WHY models disagree"""

        analysis = [
            "**Meta-Analysis: Why Models Disagree**\n",
            f"Original Question: {original_prompt}\n",
            f"Number of Models: {len(responses)}",
            f"Disagreements Found: {len(disagreements)}\n",
            "**Possible Reasons:**"
        ]

        # Heuristic analysis
        all_content = " ".join(r['response'].content for r in responses)

        if "opinion" in all_content.lower() or "subjective" in all_content.lower():
            analysis.append("- Question involves subjective interpretation")

        if any(len(r['response'].content) < 200 for r in responses):
            analysis.append("- Some models gave brief answers vs detailed ones")

        if "it depends" in all_content.lower():
            analysis.append("- Context-dependent answer with multiple valid approaches")

        analysis.append("\n💡 **Recommendation:** Review individual responses for nuanced perspectives.")

        return "\n".join(analysis)

    def _error_result(self, message: str) -> SynthesisResult:
        """Return error result"""
        return SynthesisResult(
            consensus_level=ConsensusLevel.CONFLICTED,
            confidence_score=0.0,
            synthesized_answer=f"❌ Error: {message}",
            individual_responses=[],
            agreements=[],
            disagreements=[]
        )

    def _single_response_result(self, response_data: Dict) -> SynthesisResult:
        """Handle single response case"""
        return SynthesisResult(
            consensus_level=ConsensusLevel.STRONG,
            confidence_score=response_data['response'].confidence,
            synthesized_answer=response_data['response'].content,
            individual_responses=[{
                'model': response_data['adapter'].model_name,
                'content': response_data['response'].content,
                'confidence': response_data['response'].confidence,
                'weight': response_data['adapter'].weight
            }],
            agreements=[],
            disagreements=[]
        )

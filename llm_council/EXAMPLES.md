# 📖 LLM Council - Usage Examples

Real-world examples of how to use LLM Council effectively.

---

## 🎯 Basic Queries

### 1. Technical Explanations

```bash
python cli.py ask "Explain microservices architecture"
```

**Best for:**
- Learning new concepts
- Getting multiple perspectives
- Understanding complex topics

---

### 2. Comparative Analysis

```bash
python cli.py ask "Compare REST API vs GraphQL - which should I use?"
```

**Output includes:**
- Individual model opinions
- Common agreements (e.g., "Both agree GraphQL is more flexible")
- Disagreements (e.g., "Claude prefers REST for simplicity, GPT prefers GraphQL")
- Synthesized recommendation

---

### 3. Code Review / Best Practices

```bash
python cli.py ask "Is it a good practice to use 'any' type in TypeScript?"
```

**Consensus helps with:**
- Avoiding bad practices
- Understanding trade-offs
- Industry standard approaches

---

## 🧪 Advanced Use Cases

### 4. Decision Making

```bash
python cli.py ask "Should I migrate from JavaScript to TypeScript for a 50k LOC project?"
```

**Why consensus matters:**
- Decision has high impact
- Need balanced view from multiple perspectives
- Models might disagree on migration strategy

---

### 5. Debugging / Problem Solving

```bash
python cli.py ask "Why does my React component re-render infinitely when using useEffect?"
```

**Benefit:**
- Multiple potential root causes identified
- Different debugging approaches suggested
- Consensus on most likely cause

---

### 6. Learning Paths

```bash
python cli.py ask "What's the best roadmap to learn AWS for a Python developer?"
```

**Synthesis provides:**
- Common learning steps all models agree on
- Alternative approaches from different models
- Prioritized learning path based on consensus

---

## ⚙️ Configuration Examples

### 7. Custom Weights

Edit `config.yaml`:

```yaml
models:
  claude:
    weight: 1.5  # Trust Claude more for code-related questions

  gemini:
    weight: 0.8  # Lower weight for Gemini

  gpt4:
    weight: 1.2
```

Then ask:
```bash
python cli.py ask "What are SOLID principles in OOP?"
```

Claude's answer will have 50% more influence in the synthesis.

---

### 8. Minimal Response (Fast Mode)

```bash
python cli.py ask "What is Docker?" --hide-individual
```

**Output:**
- Only synthesized answer (no individual responses)
- Faster to read
- Better for quick queries

---

### 9. Custom Config File

Create `quick_config.yaml`:

```yaml
models:
  gemini:
    enabled: true
    weight: 1.0

  gpt4:
    enabled: false  # Disable expensive model

synthesis:
  method: majority_vote  # Simple voting
  enable_meta_analysis: false
```

Use it:
```bash
python cli.py ask "Explain async" --config quick_config.yaml
```

---

## 🎭 Consensus Scenarios

### Strong Consensus (95%+ agreement)

**Input:**
```bash
python cli.py ask "What is 2 + 2?"
```

**Output:**
```
✅ STRONG CONSENSUS (Confidence: 100%)

All models agree: The answer is 4.
```

---

### Moderate Consensus (70% agreement)

**Input:**
```bash
python cli.py ask "Is Python faster than JavaScript?"
```

**Output:**
```
⚠️ MODERATE CONSENSUS (Confidence: 72%)

Common Points:
- JavaScript is generally faster for web operations
- Python is easier to write
- Performance depends on use case

Disagreements:
- Claude says: "Python with PyPy can match JS speed"
- GPT-4 says: "JavaScript V8 engine is consistently faster"
```

---

### Conflicted (No consensus)

**Input:**
```bash
python cli.py ask "What is the best programming language?"
```

**Output:**
```
⚡ CONFLICTED (Confidence: 35%)

Models have contradictory answers:
- Claude: "Python for versatility"
- GPT-4: "JavaScript for web dominance"
- Gemini: "Depends entirely on use case"

Meta-Analysis:
Question involves subjective interpretation.
No objective best answer exists.

Recommendation: Review individual responses for context.
```

---

## 🔬 Research Use Cases

### 10. Literature Review

```bash
python cli.py ask "Summarize recent advances in transformer models (2023-2024)"
```

**Synthesis:**
- Combines knowledge from multiple models
- Reduces hallucinations (if one model makes something up, others won't confirm)
- More comprehensive overview

---

### 11. Fact Checking

```bash
python cli.py ask "What was the first programming language?"
```

**Benefit:**
- If models disagree, you know the answer is disputed
- Strong consensus = likely accurate
- Weak consensus = needs more research

---

## 💡 Pro Tips

### 12. Iterative Refinement

First query:
```bash
python cli.py ask "Explain neural networks"
```

After reading synthesis, ask follow-up:
```bash
python cli.py ask "How do backpropagation algorithms work in neural networks?"
```

---

### 13. Use for Code Generation

```bash
python cli.py ask "Write a Python function to validate email addresses using regex"
```

**Why consensus helps:**
- Multiple implementation approaches
- Different models catch different edge cases
- Synthesis combines best practices

---

### 14. Philosophical Questions

```bash
python cli.py ask "Should AI be regulated?"
```

**Perfect use case:**
- No objectively correct answer
- Models represent different viewpoints
- Synthesis shows common ground and disagreements
- Meta-analysis explains WHY they disagree

---

## 🎓 Educational Use

### 15. Study Aid

```bash
python cli.py ask "Explain Big O notation with examples"
```

**Learning benefit:**
- Multiple explanations help different learning styles
- Common points = core concepts
- Disagreements = nuanced understanding

---

### 16. Interview Prep

```bash
python cli.py ask "Common Node.js interview questions and answers"
```

**Synthesis provides:**
- Comprehensive list from multiple sources
- Validated answers (consensus-based)
- Alternative explanations for tricky concepts

---

## 🚀 Production Use

### 17. Documentation Generation

```bash
python cli.py ask "Write API documentation for a user authentication endpoint"
```

**Benefit:**
- Multiple documentation styles
- Consensus on essential sections
- Comprehensive coverage

---

### 18. Code Review Assistance

```bash
python cli.py ask "Review this function for security issues: [paste code]"
```

**Why multiple models:**
- Different security expertise
- One model might catch what others miss
- Consensus on critical issues

---

## 🎯 Tips for Best Results

1. **Be specific**: "Explain closures in JavaScript" > "Explain closures"
2. **Ask for comparisons**: "Compare X vs Y" gets better synthesis
3. **Include context**: "For a beginner..." or "In production environment..."
4. **Use for validation**: Ask same question twice, see if consensus changes
5. **Trust weak consensus**: If models disagree, the answer is nuanced!

---

**Experiment and find what works for your use case!**

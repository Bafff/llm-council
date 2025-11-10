# 🤖 LLM Council

**Multi-model AI consensus system** - Get validated answers from multiple LLMs simultaneously.

Instead of asking Claude, then GPT, then Gemini separately, ask them all at once and get a **consensus answer** with automatic conflict resolution.

---

## ✨ Features

- **🔄 Parallel Querying** - Query 4+ models simultaneously (Claude, GPT-4, Gemini, Grok)
- **⚖️ Consensus Building** - Automatic synthesis of agreements and disagreements
- **🎯 Weighted Voting** - Models are weighted by reliability
- **🔍 Meta-Analysis** - Understand WHY models disagree
- **💰 Cost-Effective** - Use FREE Gemini API + cheap OpenRouter
- **🎨 Beautiful CLI** - Rich terminal UI with progress bars

---

## 🚀 Quick Start

### 1. Install

```bash
cd llm-council
pip install -r requirements.txt
```

### 2. Setup API Keys

**Option A: Interactive Setup (Easiest)**
```bash
python cli.py setup
```

**Option B: Manual Setup**

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

```env
# At minimum, get Gemini (100% FREE):
GOOGLE_API_KEY=your_key_here  # Get from https://ai.google.dev/

# Optional (for full council):
ANTHROPIC_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
```

### 3. Ask a Question!

```bash
python cli.py ask "What is the best way to learn async programming?"
```

---

## 📖 Usage

### Basic Query

```bash
python cli.py ask "Should I use TypeScript or JavaScript for my next project?"
```

### Hide Individual Responses (show only synthesis)

```bash
python cli.py ask "Explain quantum computing" --hide-individual
```

### List Available Models

```bash
python cli.py models
```

### Check Configuration

```bash
python cli.py config
```

---

## 🎯 Example Output

```
🤖 LLM Council
Question: What is async/await?

Querying 4 models in parallel...

⠋ Claude Sonnet 4.5 ━━━━━━━━━━━━━━━━━━━━ 100%
✓ Gemini 2.0 Flash (450ms) ━━━━━━━━━━━━━ 100%
✓ GPT-4 Turbo (620ms) ━━━━━━━━━━━━━━━━━ 100%
✓ Grok Beta (580ms) ━━━━━━━━━━━━━━━━━━━ 100%

⚖️ Synthesizing consensus...

╔══════════════════════════════════════════╗
║ ✅ STRONG CONSENSUS (Confidence: 92.5%)  ║
╚══════════════════════════════════════════╝

🎯 Synthesized Answer:

✅ **Strong Consensus** - All models largely agree:

**Common Points:**
1. Multiple models agree: async/await is syntactic sugar for Promises
2. Multiple models agree: Makes asynchronous code look synchronous
3. Multiple models agree: Improves code readability and error handling

**Synthesized Answer (based on Claude Sonnet 4.5):**
async/await is a modern JavaScript feature that allows you to write
asynchronous code in a synchronous style. The `async` keyword declares
an asynchronous function, and `await` pauses execution until a Promise
resolves...

[Individual responses shown below]
```

---

## 🎨 Architecture

Inspired by `claude-code-council` multi-agent system:

```
Your Question
     ↓
┌────────────────────┐
│  LLMCouncil        │  ← Orchestrator
│  (parallel exec)   │
└────────────────────┘
     ↓
┌────┬────┬────┬────┐
│Claude│Gemini│GPT│Grok│  ← Adapters (async)
└────┴────┴────┴────┘
     ↓
┌────────────────────┐
│ ConsensusSynthesizer│ ← Weighted voting + conflict resolution
└────────────────────┘
     ↓
  Final Answer
```

---

## 💰 Costs

| Model | Cost per 1K tokens | How to Access |
|-------|-------------------|---------------|
| **Gemini 2.0** | FREE! (60 req/min) | https://ai.google.dev/ |
| GPT-4 Turbo | $0.002 (via OpenRouter) | https://openrouter.ai/ |
| Claude Sonnet | $0.003 (via OpenRouter) | https://openrouter.ai/ |
| Grok Beta | $0.0005 (via OpenRouter) | https://openrouter.ai/ |

**Example:** 100 queries (4 models each) = ~$1-2

---

## 🔧 Configuration

Edit `config.yaml` to:
- Enable/disable models
- Adjust consensus weights
- Change synthesis method (weighted_consensus, majority_vote, debate)
- Configure output format

```yaml
models:
  claude:
    enabled: true
    weight: 1.2  # Higher weight = more influence

synthesis:
  method: weighted_consensus
  strong_consensus: 0.8  # 80% agreement threshold
```

---

## 🛠️ Advanced Usage

### Use Custom Config

```bash
python cli.py ask "question" --config my_config.yaml
```

### Integration with Other Scripts

```python
from llm_council.core.council import LLMCouncil
import asyncio

async def main():
    council = LLMCouncil()
    result = await council.query("What is FastAPI?")
    print(result.synthesized_answer)

asyncio.run(main())
```

---

## 🚦 Roadmap

- [x] Parallel multi-model querying
- [x] Consensus synthesis
- [x] CLI interface
- [ ] Web UI for non-technical users
- [ ] Browser cookie auth (free access to Claude/GPT)
- [ ] Claude Code session integration
- [ ] Debate mode (models argue with each other)
- [ ] History and analytics

---

## 🤝 Contributing

Based on concepts from:
- **claude-code-council** - Multi-agent code review system
- **ChatALL** - Multi-model desktop app

---

## 📄 License

MIT License - feel free to use and modify!

---

## 🆘 Troubleshooting

**"No models available"**
- Run `python cli.py setup` to configure API keys
- Check `.env` file exists and has correct keys
- At minimum, get free Gemini key

**"Module not found"**
- Run `pip install -r requirements.txt`
- Make sure you're in `llm-council/` directory

**"Authentication failed"**
- Verify your API keys are correct
- Check https://ai.google.dev/ for Gemini
- Check https://openrouter.ai/ for others

---

**Made with ❤️ for people who want validated AI answers**

**Version**: 1.0.0 MVP

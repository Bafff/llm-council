# 🚀 Installation Guide - LLM Council

Quick setup guide to get you running in 5 minutes!

---

## Prerequisites

- Python 3.9+ (check: `python --version`)
- pip (check: `pip --version`)

---

## Step 1: Install Dependencies

```bash
cd llm-council
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude SDK
- `google-generativeai` - Gemini SDK (FREE!)
- `openai` - OpenAI/OpenRouter SDK
- `rich` - Beautiful CLI
- `typer` - CLI framework
- Other utilities

---

## Step 2: Get API Keys

### Option A: Gemini Only (100% FREE!)

1. Go to https://ai.google.dev/
2. Click "Get API key"
3. Create new project
4. Copy your API key

```bash
# Create .env file
echo "GOOGLE_API_KEY=your_key_here" > .env
```

**You're done!** You can now use Gemini for free.

### Option B: Full Council (Recommended)

Get keys for all models:

1. **Gemini (FREE)**: https://ai.google.dev/
   - 60 requests/minute
   - No credit card needed

2. **OpenRouter ($1-5 for testing)**:
   - Go to https://openrouter.ai/
   - Sign up
   - Add $1-5 credits
   - Get API key
   - Access to GPT-4, Claude, Grok, 100+ models

3. **Claude (Optional)**:
   - Go to https://console.anthropic.com/
   - Add payment method
   - Get API key

Create `.env`:
```bash
GOOGLE_API_KEY=AIzaSy...
OPENROUTER_API_KEY=sk-or-v1-...
ANTHROPIC_API_KEY=sk-ant-...
```

**OR use interactive setup:**
```bash
python cli.py setup
```

---

## Step 3: Test Installation

```bash
python cli.py models
```

Should show:
```
🤖 LLM Council Models
┌─────────────────┬─────────────┬────────┬──────────┐
│ Model           │ Status      │ Weight │ Adapter  │
├─────────────────┼─────────────┼────────┼──────────┤
│ Gemini 2.0      │ ✓ Available │ 1.0    │ Gemini.. │
│ Claude Sonnet   │ ✓ Available │ 1.2    │ Claude.. │
│ ...             │             │        │          │
└─────────────────┴─────────────┴────────┴──────────┘
```

---

## Step 4: Ask Your First Question!

```bash
python cli.py ask "What is the difference between async and sync programming?"
```

You should see:
1. Progress bars as models respond
2. Individual responses (if enabled)
3. Synthesized consensus answer
4. Meta-analysis of agreements/disagreements

---

## 🎉 You're Ready!

Try these:

```bash
# Compare programming languages
python cli.py ask "Should I use Python or Go for web APIs?"

# Get technical explanations
python cli.py ask "Explain Docker containers in simple terms"

# Make decisions
python cli.py ask "What's the best way to learn machine learning?"

# Hide individual responses (faster)
python cli.py ask "What is recursion?" --hide-individual
```

---

## 🔧 Troubleshooting

### "No module named 'anthropic'"
```bash
pip install -r requirements.txt
```

### "No models available"
- Check your `.env` file exists
- Verify API keys are correct
- At minimum, get free Gemini key

### "Rate limit exceeded" (Gemini)
- Gemini free tier: 60 requests/minute
- Wait a minute and try again
- Or use paid models

### Import errors
Make sure you're in the correct directory:
```bash
cd /path/to/llm-council
pwd  # Should show .../llm-council
python cli.py models
```

---

## 📚 Next Steps

1. **Read README.md** for full documentation
2. **Edit config.yaml** to customize behavior
3. **Try advanced features**:
   ```bash
   python cli.py config  # View configuration
   python cli.py --help  # See all commands
   ```

---

## 🚀 Advanced: System-Wide Install

Make `llm-council` available everywhere:

```bash
# Option 1: Symlink (recommended)
ln -s /path/to/llm-council/cli.py ~/bin/llm-council
chmod +x ~/bin/llm-council

# Then use anywhere:
llm-council ask "anything"

# Option 2: Alias (add to ~/.bashrc or ~/.zshrc)
alias llm="python /path/to/llm-council/cli.py"
```

---

**Need help? Check README.md or open an issue!**

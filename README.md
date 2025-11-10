# Claude Code Council + LLM Council 🤖

This repository contains **two powerful AI systems**:

1. **Claude Code Council** - Multi-agent code review system
2. **LLM Council** - Multi-model AI consensus system ✨

---

## 🆕 LLM Council - Multi-Model Consensus System

**Get validated answers from Claude, GPT-4, Gemini, and Grok simultaneously!**

Instead of asking each model separately, ask them all at once and get:
- ✅ Consensus analysis
- ⚖️ Weighted voting
- 🔍 Meta-analysis of disagreements
- 🎯 Synthesized final answer

### ⚡ Quick Install

```bash
# One command installation
bash install.sh
```

### 🚀 Usage

```bash
# Ask a question
llm-council ask "What is the best way to learn Python?"

# Or short syntax
council "Explain async/await"

# List available models
llm-council models

# Setup API keys
llm-council setup
```

### 🔑 Authentication - NEW: CLI Session Support!

**Use your existing CLI subscriptions instead of API keys!** Save costs by leveraging Claude Code CLI, ChatGPT CLI, and other tools you already have installed.

**Automatic CLI Authentication:**
```bash
# No API keys needed if you have CLI tools installed and authenticated!
# LLM Council will automatically use:
# - Claude Code CLI session
# - ChatGPT CLI (shell_gpt) session
# - Gemini via gcloud CLI
# - Falls back to API keys if CLI auth unavailable
```

**Supported CLI Tools:**
- Claude Code CLI (`claude`)
- Anthropic CLI (`anthropic`)
- ChatGPT CLI (`chatgpt`, `sgpt`)
- OpenAI CLI (`openai`)
- Gemini CLI (`gemini`)
- Google Cloud CLI (`gcloud`)

**Priority:** CLI Session → API Keys (automatic fallback)

See [CLI_AUTH.md](CLI_AUTH.md) for detailed setup and usage.

### 📚 Documentation

- **[Main README](llm_council/README.md)** - Full documentation
- **[Quick Start](llm_council/QUICKSTART.md)** - Fast setup guide
- **[Update Guide](llm_council/UPDATE_GUIDE.md)** - Development workflow
- **[Install Guide](llm_council/INSTALL_PIPX.md)** - Pipx installation details
- **[Examples](llm_council/EXAMPLES.md)** - 18 usage examples
- **[Changelog](llm_council/CHANGELOG.md)** - Version history

### 🔄 After Each Code Change

```bash
pipx reinstall llm_council && llm-council version
```

That's it! Changes applied.

---

## 📦 Claude Code Council (Original)

AI-powered multi-agent code review system for Claude Code.

See original README below for details.

---

# Claude Code Council (Original Project)

**AI-powered multi-agent code review system for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue.svg)](https://github.com/646826/claude-code-council)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/646826/claude-code-council)

Get intelligent, evidence-based code reviews from 5 specialized AI agents working in parallel. Catch security issues, enforce DRY principles, protect your APIs, and maintain architectural consistency—all before you commit.

[Continue reading original README...]

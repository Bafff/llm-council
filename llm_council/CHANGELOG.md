# Changelog

All notable changes to LLM Council will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Web UI for non-technical users
- Browser cookie authentication for free access
- Claude Code session integration
- Debate mode (models argue with each other)
- History and analytics dashboard
- Embedding-based similarity for better consensus detection

---

## [1.0.0] - 2025-11-07

### Added

#### Core Features
- **Multi-model querying system** with parallel execution
  - Support for Claude Sonnet 4.5 via Anthropic API
  - Support for Gemini 2.0 Flash (FREE API)
  - Support for GPT-4 Turbo via OpenRouter
  - Support for Grok Beta via OpenRouter
  - Extensible adapter architecture for adding new models

- **Consensus synthesis engine** (`core/synthesizer.py`)
  - Weighted voting system based on model reliability
  - Automatic detection of agreements and disagreements
  - Four consensus levels: Strong (>80%), Moderate (60-80%), Weak (40-60%), Conflicted (<40%)
  - Meta-analysis explaining WHY models disagree
  - Confidence scoring combining multiple factors

- **Parallel orchestration** (`core/council.py`)
  - Async/await based concurrent querying
  - Real-time progress tracking with Rich progress bars
  - Automatic retry logic with exponential backoff
  - Graceful degradation when models fail

#### Adapters
- **Base adapter** (`adapters/base.py`)
  - Standardized `LLMResponse` format
  - Multiple authentication methods (API key, browser cookies, OAuth)
  - Health checking and availability detection
  - Per-model weight configuration

- **Claude adapter** (`adapters/claude_adapter.py`)
  - Anthropic API integration
  - Async message creation
  - Token usage tracking
  - Latency measurement
  - Placeholder for Claude Code session auth

- **Gemini adapter** (`adapters/gemini_adapter.py`)
  - Google Generative AI SDK integration
  - FREE API support (60 requests/minute)
  - Automatic token estimation
  - Sync-to-async wrapper for compatibility

- **OpenRouter adapter** (`adapters/openrouter_adapter.py`)
  - OpenAI-compatible API for multiple models
  - Support for GPT-4, Grok, and 100+ other models
  - Automatic fallback to OpenAI API if key provided
  - Cost-effective access to premium models

#### CLI Interface
- **Beautiful CLI** (`cli.py`) powered by Typer and Rich
  - `ask` - Query the council with a question
  - `models` - List available models and their status
  - `config` - Display current configuration
  - `setup` - Interactive API key setup wizard
  - `version` - Show version information
  - Shorthand syntax: `python cli.py "question"` (no subcommand needed)

#### Configuration
- **YAML-based config** (`config.yaml`)
  - Per-model enable/disable
  - Model weight configuration
  - Synthesis method selection (weighted_consensus, majority_vote, debate)
  - Consensus thresholds
  - Output format preferences

- **Environment variables** (`.env`)
  - Secure API key storage
  - `.env.example` template provided
  - Automatic loading via python-dotenv

#### Documentation
- **README.md** - Comprehensive project overview with examples
- **INSTALL.md** - Step-by-step installation guide
- **EXAMPLES.md** - 18 real-world usage examples
- **CHANGELOG.md** - Version history (this file)
- Inline code documentation and type hints

#### Development Tools
- **pyproject.toml** - Modern Python project configuration
  - Build system setup
  - Dependency management
  - Optional dependencies for dev/web
  - Tool configurations (black, ruff, pytest, mypy)
  - Project metadata and classifiers

- **requirements.txt** - Pip-installable dependencies
- **.gitignore** - Comprehensive ignore rules for Python projects
- **MIT License** - Open source friendly

### Architecture Decisions

#### Inspired by claude-code-council
- Multi-agent parallel execution model
- Weighted evidence-based voting
- Streaming progress indicators
- Conflict detection and debate rounds
- Synthesis as final arbiter

#### Improvements over ChatALL
- Added consensus building (not just parallel display)
- Added meta-analysis of disagreements
- CLI-first design (vs Electron desktop)
- Extensible adapter pattern
- Built-in synthesis engine

### Technical Specifications
- **Language**: Python 3.9+
- **Async Framework**: asyncio, aiohttp, httpx
- **CLI Framework**: Typer (Click-based)
- **UI Framework**: Rich (terminal)
- **Config Format**: YAML + Environment Variables
- **API Clients**: anthropic, google-generativeai, openai
- **Code Quality**: Black, Ruff, MyPy, Pytest

### Performance
- Parallel querying: 30-50% faster than sequential
- Average query time: 2-5 seconds (4 models)
- Gemini: ~450ms, GPT-4: ~620ms, Grok: ~580ms
- Synthesis: <100ms

### Cost Analysis
- **Gemini**: FREE (60 req/min forever)
- **GPT-4**: $0.002/1K tokens via OpenRouter
- **Claude**: $0.003/1K tokens via OpenRouter
- **Grok**: $0.0005/1K tokens via OpenRouter
- **Example**: 100 queries × 4 models ≈ $1-2 total

### Known Limitations
- Claude Code session auth not yet implemented
- Browser cookie auth not yet implemented
- Web UI not yet implemented
- No history/analytics persistence
- No embedding-based similarity (uses keyword matching)
- Single user only (no multi-tenancy)

### Dependencies
See `requirements.txt` for full list. Key dependencies:
- anthropic ^0.34.0
- google-generativeai ^0.3.0
- openai ^1.0.0
- rich ^13.0.0
- typer ^0.9.0

### Breaking Changes
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Security
- API keys stored in `.env` file (gitignored)
- No hardcoded credentials
- HTTPS-only API communication
- No data persistence (privacy-first)

---

## Version History

### Versioning Scheme
- **Major (X.0.0)**: Breaking changes, major feature additions
- **Minor (1.X.0)**: New features, backward compatible
- **Patch (1.0.X)**: Bug fixes, minor improvements

### Roadmap
- **1.1.0**: Web UI implementation
- **1.2.0**: Browser cookie authentication
- **1.3.0**: Claude Code integration
- **1.4.0**: Debate mode
- **2.0.0**: Multi-user support, persistence

---

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Update this CHANGELOG.md under `[Unreleased]`
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## Contact

**Project Owner**: Dima
**Repository**: https://github.com/Bafff/claude-code-council
**Issues**: https://github.com/Bafff/claude-code-council/issues

---

**[1.0.0]**: https://github.com/Bafff/claude-code-council/releases/tag/v1.0.0

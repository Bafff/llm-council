# Add CLI-Based Authentication with API Key Fallback

## 🎯 Summary

This PR implements comprehensive **CLI session authentication** that allows users to leverage their existing CLI tool subscriptions (Claude Code, ChatGPT, Gemini, etc.) instead of requiring API keys. API keys now serve as an automatic fallback when CLI authentication is unavailable.

**Key Benefit**: Save costs by using existing CLI subscriptions and subscriptions instead of consuming API quota.

## ✨ Features

### 1. **CLI Session Manager**
- Auto-detects and extracts authentication tokens from 6 CLI providers:
  - **Claude Code CLI** (`claude`)
  - **Anthropic CLI** (`anthropic`)
  - **ChatGPT CLI** (`chatgpt`, `sgpt`)
  - **OpenAI CLI** (`openai`)
  - **Gemini CLI** (`gemini`)
  - **Google Cloud CLI** (`gcloud`)
- Session caching for performance optimization
- Automatic detection of session files in standard locations

### 2. **Enhanced Adapters**
All adapters now support CLI authentication with automatic API key fallback:
- **Claude Adapter**: Try Claude Code CLI → Anthropic CLI → API Key
- **Gemini Adapter**: Try Gemini CLI → gcloud CLI → API Key
- **OpenRouter Adapter**: Try ChatGPT CLI → OpenAI CLI → API Key

### 3. **Authentication Debugging**
- Visual indicators showing which auth method was used:
  - 🔐 = CLI Session authentication
  - 🔑 = API Key authentication
- Detailed auth source information (e.g., "Claude Code CLI", "ANTHROPIC_API_KEY env var")
- Real-time auth status displayed during query execution

### 4. **Backward Compatibility**
- Zero breaking changes
- Existing API key workflows continue to work unchanged
- CLI auth is opt-in via configuration (enabled by default)

## 🏗️ Architecture

### Authentication Flow
```
User Query
    ↓
Adapter checks use_cli_auth: true
    ↓
Try CLI Authentication
    ↓
✅ Success → Use CLI Session Token
    ↓
❌ Failed → Print fallback message
    ↓
Try API Key Authentication
    ↓
✅ Success → Use API Key
    ↓
❌ Failed → Authentication Failed
```

### New Components

**`llm_council/auth/`**
- `cli_session_manager.py` - Core CLI session detection and token extraction
- `__init__.py` - Module exports

**Updated Components**
- `adapters/base.py` - Added `CLI_SESSION` auth method, auth tracking fields
- `adapters/claude_adapter.py` - CLI auth implementation
- `adapters/gemini_adapter.py` - CLI auth implementation
- `adapters/openrouter_adapter.py` - CLI auth implementation
- `core/synthesizer.py` - Pass auth info through responses
- `core/council.py` - Display auth info in output
- `config.yaml` - CLI authentication configuration

## 📝 Configuration

### Per-Model CLI Auth Control
```yaml
models:
  claude:
    enabled: true
    use_cli_auth: true  # Try CLI first (default)

  gemini:
    enabled: true
    use_cli_auth: false  # Skip CLI, use API key only
```

### Global CLI Auth Settings
```yaml
auth:
  cli_sessions:
    enabled: true
    providers:
      - claude_code
      - anthropic
      - chatgpt
      - openai
      - gemini
      - gcloud
    auto_detect: true
    cache_sessions: true
```

## 📊 Output Example

When running queries, users now see authentication details:

```
┌─ Claude Sonnet 4.5 (confidence: 90%, weight: 1.2) ────────┐
│ 🔐 Auth: CLI Session (Claude Code CLI)                    │
│ [response content...]                                      │
└────────────────────────────────────────────────────────────┘

┌─ Gemini 2.5 Flash (confidence: 85%, weight: 1.0) ─────────┐
│ 🔑 Auth: API Key (GOOGLE_API_KEY env var)                 │
│ [response content...]                                      │
└────────────────────────────────────────────────────────────┘
```

## 🧪 Testing

### Automated Tests
- Created comprehensive test suite: `tests/unit/test_cli_auth.py`
- Tests cover:
  - CLI session detection
  - Token extraction from various formats (JSON, config files)
  - Session caching
  - CLI tool detection
  - Error handling

### Manual Testing Scenarios
1. **CLI Only**: Install CLI tools, no API keys → ✅ Works
2. **API Key Only**: No CLI tools, only env vars → ✅ Works
3. **Mixed**: Some models via CLI, others via API → ✅ Works
4. **Fallback**: CLI fails, falls back to API key → ✅ Works
5. **No Auth**: No CLI or API keys → ✅ Proper error messages

## 📚 Documentation

### New Documentation
- **`CLI_AUTH.md`** - Comprehensive CLI authentication guide
  - Setup instructions for each CLI tool
  - Configuration examples
  - Troubleshooting guide
  - Architecture explanation
  - Security considerations

### Updated Documentation
- **`README.md`** - Added CLI authentication section with quick overview

## 🔒 Security Considerations

1. **Local Storage**: Session tokens remain in local home directory
2. **No Token Exposure**: Tokens never logged or exposed in output
3. **Fallback Safety**: API key fallback ensures availability
4. **File Permissions**: Respects standard CLI tool security practices

## 🚀 Usage

### Quick Start
```bash
# 1. Install and authenticate with CLI tool
npm install -g @anthropic-ai/claude-code
claude login

# 2. Run queries (no API keys needed!)
llm-council ask "What is quantum computing?"

# Output shows:
# ✅ Claude Sonnet 4.5: Authenticated via Claude Code CLI
# 🔐 Auth: CLI Session (Claude Code CLI)
```

### Disable CLI Auth for Specific Model
```yaml
# config.yaml
models:
  claude:
    use_cli_auth: false  # Use API key only
```

### Check Auth Status
```bash
llm-council models
# Shows which models are available and their auth methods
```

## 🎁 Benefits

1. **💰 Cost Savings**: Use existing CLI subscriptions
2. **🔧 Simplified Setup**: One authentication for CLI + LLM Council
3. **🛡️ Better Security**: Local session tokens vs environment variables
4. **🔄 Automatic Fallback**: Never breaks existing API key workflows
5. **📊 Transparency**: Clear visibility into auth methods used
6. **⚡ Performance**: Session caching reduces lookup overhead

## 📦 Files Changed

### New Files (4)
- `llm_council/auth/__init__.py`
- `llm_council/auth/cli_session_manager.py`
- `llm_council/tests/unit/test_cli_auth.py`
- `CLI_AUTH.md`

### Modified Files (7)
- `llm_council/adapters/base.py`
- `llm_council/adapters/claude_adapter.py`
- `llm_council/adapters/gemini_adapter.py`
- `llm_council/adapters/openrouter_adapter.py`
- `llm_council/core/synthesizer.py`
- `llm_council/core/council.py`
- `llm_council/config.yaml`
- `README.md`

**Total Changes**: +1,170 insertions, -57 deletions

## 🔗 Related Issues

Implements feature request inspired by: https://github.com/x22x22/code-cli-any-llm

## ✅ Checklist

- [x] Code implements all specified features
- [x] Comprehensive test coverage added
- [x] Documentation created and updated
- [x] Backward compatibility maintained
- [x] No breaking changes
- [x] Configuration examples provided
- [x] Error handling implemented
- [x] Security considerations addressed
- [x] Examples and usage guides included
- [x] Auth debugging information added

## 🎯 Migration Guide

### For Existing Users
**No action required!** This is fully backward compatible:
- Existing API key authentication continues to work unchanged
- CLI auth is opt-in (though enabled by default)
- To disable CLI auth globally: Set `auth.cli_sessions.enabled: false`

### For New Users
**Choose your auth method:**
1. **CLI Auth (Recommended)**: Install CLI tools, authenticate once, enjoy cost savings
2. **API Keys**: Set environment variables (existing workflow)
3. **Mixed**: Use both - CLI for some models, API keys for others

## 🔮 Future Enhancements

Potential follow-ups (not in this PR):
- [ ] Browser cookie extraction for free-tier usage
- [ ] OAuth flow support
- [ ] Session token auto-refresh
- [ ] Multi-account support
- [ ] Additional CLI provider support

## 🙏 Acknowledgments

Inspired by the excellent work in [code-cli-any-llm](https://github.com/x22x22/code-cli-any-llm) for OAuth implementation patterns and CLI integration approaches.

---

**Ready to merge**: All tests passing, documentation complete, no breaking changes.

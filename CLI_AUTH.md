# CLI Authentication Guide

## Overview

LLM Council now supports **CLI-based authentication**, allowing you to use your existing CLI tool subscriptions instead of managing API keys. This saves costs by leveraging your Claude Code, ChatGPT, Gemini, and other CLI subscriptions.

## How It Works

### Priority Order

1. **CLI Session** (Primary) - Extract authentication from installed CLI tools
2. **API Keys** (Fallback) - Use environment variables if CLI auth unavailable

### Supported CLI Tools

| Provider | CLI Tools Supported | Configuration Files |
|----------|---------------------|---------------------|
| **Claude** | `claude`, `anthropic` | `~/.claude/session.json`<br>`~/.config/claude/session.json`<br>`~/.anthropic/session.json` |
| **ChatGPT/OpenAI** | `chatgpt`, `sgpt`, `openai` | `~/.config/shell_gpt/.sgptrc`<br>`~/.config/chatgpt/config.json`<br>`~/.openai/config.json` |
| **Gemini** | `gemini`, `gcloud` | `~/.gemini/config.json`<br>`~/.config/gcloud/application_default_credentials.json` |

## Setup

### 1. Install CLI Tools (Recommended)

To use CLI authentication, install and authenticate with at least one CLI tool:

**Claude Code CLI:**
```bash
# Install Claude Code CLI (if not already installed)
npm install -g @anthropic-ai/claude-code

# Authenticate
claude login
```

**ChatGPT CLI (shell_gpt):**
```bash
# Install shell_gpt
pipx install shell-gpt

# Configure with your API key (one-time setup)
sgpt --api-key YOUR_OPENAI_API_KEY
```

**Gemini via gcloud:**
```bash
# Install gcloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth application-default login
```

### 2. Enable CLI Authentication

CLI authentication is **enabled by default** in `config.yaml`:

```yaml
# Models configuration
models:
  claude:
    enabled: true
    use_cli_auth: true  # Try CLI first, fallback to API key

  gemini:
    enabled: true
    use_cli_auth: true

  gpt4:
    enabled: true
    use_cli_auth: true

# Authentication configuration
auth:
  cli_sessions:
    enabled: true
    auto_detect: true
    cache_sessions: true
```

### 3. Use LLM Council

Just run your queries - CLI authentication happens automatically:

```bash
llm-council ask "What is the meaning of life?"
```

You'll see authentication status for each model:
```
✅ Claude Sonnet 4.5: Authenticated via Claude Code CLI
✅ Gemini 2.5 Flash: Authenticated via gcloud CLI
ℹ️  GPT-4 Turbo: CLI auth unavailable, trying API key...
✅ GPT-4 Turbo: Authenticated via API key
```

## Configuration

### Disable CLI Authentication for Specific Models

Edit `config.yaml`:

```yaml
models:
  claude:
    use_cli_auth: false  # Always use API key for Claude
```

### Disable CLI Authentication Globally

```yaml
auth:
  cli_sessions:
    enabled: false  # Use only API keys
```

### Custom Session Paths

The CLI session manager auto-detects standard locations. If your CLI tools store sessions elsewhere, you can modify the detection logic in:

`llm_council/auth/cli_session_manager.py`

## Authentication Flow

### Example: Claude Adapter

```
1. User runs: llm-council ask "Hello"
   ↓
2. Claude Adapter checks: use_cli_auth = true?
   ↓
3. Try CLI authentication:
   - Check Claude Code CLI session files
   - Check Anthropic CLI session files
   - Extract API key/token
   ↓
4. If successful: ✅ Authenticated via CLI
   ↓
5. If failed: Try API key from environment
   - Check ANTHROPIC_API_KEY
   ↓
6. If successful: ✅ Authenticated via API key
   ↓
7. If failed: ⚠️ Authentication failed
```

## Benefits

1. **Cost Savings** - Use existing CLI subscriptions instead of separate API keys
2. **Simplified Management** - No need to manage multiple API keys
3. **Automatic Fallback** - Falls back to API keys if CLI auth unavailable
4. **Security** - Session tokens stored locally, not in environment variables

## Troubleshooting

### "CLI auth unavailable"

**Cause:** CLI tool not installed or not authenticated

**Solution:**
1. Install the CLI tool (see Setup section)
2. Authenticate with the CLI tool
3. Verify session files exist in standard locations

### "No API key found"

**Cause:** Both CLI auth and API key auth failed

**Solution:**
1. **Option 1 (Recommended):** Install and authenticate CLI tool
2. **Option 2:** Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   export GOOGLE_API_KEY="your-api-key"
   export OPENAI_API_KEY="your-api-key"
   ```

### Check CLI Authentication Status

```bash
# Check if Claude CLI is authenticated
claude --version
claude whoami

# Check if gcloud is authenticated
gcloud auth list

# Check if shell_gpt is configured
sgpt --version
cat ~/.config/shell_gpt/.sgptrc
```

## Implementation Details

### Architecture

```
User Request
    ↓
LLMCouncil
    ↓
Adapter (Claude/Gemini/OpenRouter)
    ↓
CLISessionManager
    ↓
Detect & Extract CLI Sessions
    ↓
[Try CLI Auth] → [Success] → Use CLI Token
    ↓
[Failure]
    ↓
[Try API Key] → [Success] → Use API Key
    ↓
[Failure]
    ↓
Authentication Failed
```

### Key Files

- `llm_council/auth/cli_session_manager.py` - CLI session detection & extraction
- `llm_council/adapters/base.py` - Base adapter with CLI_SESSION auth method
- `llm_council/adapters/claude_adapter.py` - Claude-specific CLI auth
- `llm_council/adapters/gemini_adapter.py` - Gemini-specific CLI auth
- `llm_council/adapters/openrouter_adapter.py` - OpenAI/ChatGPT CLI auth
- `llm_council/config.yaml` - Configuration settings

## Examples

### Example 1: Pure CLI Authentication

```bash
# Install CLI tools
npm install -g @anthropic-ai/claude-code
pipx install shell-gpt

# Authenticate
claude login
sgpt --api-key YOUR_KEY

# Use LLM Council (no API keys needed!)
llm-council ask "Explain quantum computing"
```

### Example 2: Mixed CLI + API Keys

```bash
# Set only Gemini API key
export GOOGLE_API_KEY="your-key"

# Use Claude via CLI, Gemini via API key
llm-council ask "Compare Python and Rust"
```

### Example 3: Disable CLI Auth

```bash
# Edit config.yaml
# Set use_cli_auth: false for all models

# Run with API keys only
export ANTHROPIC_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
llm-council ask "What is machine learning?"
```

## Security Considerations

- CLI session tokens are stored locally in your home directory
- Ensure proper file permissions on session files (`chmod 600`)
- Session tokens may expire - re-authenticate with CLI tools if needed
- API keys in environment variables are visible to all processes - use CLI auth for better security

## Future Enhancements

- [ ] Browser cookie extraction (for free-tier usage)
- [ ] OAuth flow support
- [ ] Custom session path configuration
- [ ] Session token refresh
- [ ] Multi-account support

## Contributing

Found a CLI tool that should be supported? Open an issue or PR!

Location: `llm_council/auth/cli_session_manager.py`

Add a new provider:
1. Add enum to `CLIProvider`
2. Implement `_get_<provider>_session()` method
3. Update documentation

## Related Resources

- [Example Repository](https://github.com/x22x22/code-cli-any-llm) - Inspiration for CLI auth
- [Claude Code CLI](https://docs.anthropic.com/claude/docs/claude-cli)
- [OpenAI CLI](https://github.com/openai/openai-cli)
- [shell_gpt](https://github.com/TheR1D/shell_gpt)
- [gcloud CLI](https://cloud.google.com/sdk/gcloud)

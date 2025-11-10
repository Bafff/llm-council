# Bug Fixes for CLI Authentication

## Summary

This document describes two critical bugs in the CLI authentication implementation that were identified in PR review and have been fixed using TDD methodology.

---

## Bug #1: Gemini Adapter - Incorrect gcloud Bearer Token Handling

### Problem

**Location**: `llm_council/adapters/gemini_adapter.py`

**Issue**: The Gemini adapter treated OAuth access tokens from `gcloud` as API keys, sending them in the wrong HTTP header.

- **Current behavior**: Sent gcloud tokens in `x-goog-api-key` header
- **Correct behavior**: Should send gcloud tokens in `Authorization: Bearer` header

**Impact**: CLI authentication via gcloud was completely unusable, resulting in 401/403 errors from the Gemini API.

### Root Cause

```python
# OLD CODE (lines 56-62)
session = self.cli_session_manager.get_session(CLIProvider.GOOGLE_AI)
if session.is_authenticated and (session.token or session.api_key):
    self.api_key = session.token or session.api_key  # ❌ Treats bearer token as API key
    # ...

# In query method (line 112)
headers={
    'Content-Type': 'application/json',
    'x-goog-api-key': self.api_key  # ❌ Wrong header for bearer tokens
}
```

### Solution

**Changes Made**:

1. **Added `bearer_token` field** to track OAuth tokens separately from API keys
2. **Detect token type** during authentication
3. **Use correct header** based on auth type

```python
# NEW CODE
def __init__(self, config: dict):
    # ...
    self.bearer_token: Optional[str] = None  # ✅ Separate field for OAuth tokens

def _authenticate_via_cli(self) -> bool:
    session = self.cli_session_manager.get_session(CLIProvider.GOOGLE_AI)
    if session.is_authenticated and (session.token or session.api_key):
        if session.token:  # ✅ Detect OAuth bearer token
            self.bearer_token = session.token
            self.auth_source = "gcloud CLI (OAuth Bearer Token)"
        else:
            self.api_key = session.api_key
        # ...

async def query(self, prompt: str, **kwargs) -> LLMResponse:
    # Build headers based on auth type
    headers = {'Content-Type': 'application/json'}

    if self.bearer_token:  # ✅ Use Authorization header for bearer tokens
        headers['Authorization'] = f'Bearer {self.bearer_token}'
    elif self.api_key:  # ✅ Use x-goog-api-key for API keys
        headers['x-goog-api-key'] = self.api_key
    # ...
```

### Test Coverage

Created TDD tests in `test_cli_auth_bugfixes.py`:

- `test_gcloud_token_uses_bearer_auth_header()` - Verifies bearer token uses correct header
- `test_api_key_still_uses_api_key_header()` - Ensures API keys still work

---

## Bug #2: OpenRouter Adapter - Model ID Mismatch with OpenAI CLI

### Problem

**Location**: `llm_council/adapters/openrouter_adapter.py`

**Issue**: When using OpenAI CLI authentication, the adapter switched to OpenAI's base URL but continued using OpenRouter-formatted model IDs.

- **Current behavior**: Sent `openai/gpt-4-turbo` to `api.openai.com` ❌
- **Correct behavior**: Should send `gpt-4-turbo` to `api.openai.com` ✅

**Impact**: CLI-derived OpenAI credentials produced 404/invalid model errors, preventing CLI authentication fallback from working.

### Root Cause

```python
# OLD CODE
def _authenticate_via_cli(self) -> bool:
    # ...
    base_url = "https://api.openai.com/v1"  # ✅ Correct URL
    self.client = AsyncOpenAI(api_key=self.api_key, base_url=base_url)
    # ...

async def query(self, prompt: str, **kwargs) -> LLMResponse:
    completion = await self.client.chat.completions.create(
        model=self.model_id,  # ❌ Still using "openai/gpt-4-turbo"
        # ...
    )
```

The model ID `openai/gpt-4-turbo` is OpenRouter's format. OpenAI's API only accepts `gpt-4-turbo`.

### Solution

**Changes Made**:

1. **Track base URL** to know which API is being used
2. **Add normalization method** to strip vendor prefix when needed
3. **Apply normalization** during queries

```python
# NEW CODE
def __init__(self, config: dict):
    # ...
    self.base_url: Optional[str] = None  # ✅ Track which API we're using

def _authenticate_via_cli(self) -> bool:
    # ...
    self.base_url = "https://api.openai.com/v1"  # ✅ Store base URL
    self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
    # ...

def _normalize_model_id(self) -> str:
    """
    Normalize model ID based on the base URL being used.

    OpenRouter: "openai/gpt-4-turbo" (keep prefix)
    OpenAI API: "gpt-4-turbo" (strip prefix)
    """
    if self.base_url and "api.openai.com" in self.base_url:
        # ✅ Strip vendor prefix for OpenAI API
        if '/' in self.model_id:
            vendor, model = self.model_id.split('/', 1)
            return model
        return self.model_id
    else:
        # ✅ Keep vendor prefix for OpenRouter
        return self.model_id

async def query(self, prompt: str, **kwargs) -> LLMResponse:
    model_id = self._normalize_model_id()  # ✅ Normalize before use

    completion = await self.client.chat.completions.create(
        model=model_id,  # ✅ Correct model ID for the API
        # ...
    )
```

### Test Coverage

Created TDD tests in `test_cli_auth_bugfixes.py`:

- `test_openai_cli_strips_model_prefix()` - Verifies prefix stripped for OpenAI
- `test_openrouter_keeps_model_prefix()` - Ensures OpenRouter format preserved
- `test_grok_model_rejected_with_openai_cli()` - Documents edge case

---

## Testing Methodology

Both bugs were fixed using **Test-Driven Development (TDD)**:

1. **Write failing tests** that demonstrate the bug
2. **Implement the fix** to make tests pass
3. **Verify** the fix doesn't break existing functionality

### Test Execution

Run the bug fix tests:

```bash
pytest llm_council/tests/unit/test_cli_auth_bugfixes.py -v
```

Run all authentication tests:

```bash
pytest llm_council/tests/unit/test_cli_auth*.py -v
```

---

## Files Modified

### Bug #1 Fix

- `llm_council/adapters/gemini_adapter.py`
  - Added `bearer_token` field (line 18)
  - Updated `_authenticate_via_cli()` to detect token type (lines 59-70)
  - Updated `query()` to use correct headers (lines 115-129)

### Bug #2 Fix

- `llm_council/adapters/openrouter_adapter.py`
  - Added `base_url` field (line 20)
  - Updated auth methods to track base_url (lines 50, 61, 86, 90)
  - Added `_normalize_model_id()` method (lines 105-124)
  - Updated `query()` to normalize model ID (line 140)

### Tests

- `llm_council/tests/unit/test_cli_auth_bugfixes.py` (new file)
  - 6 comprehensive TDD tests
  - Full coverage of both bugs and edge cases

---

## Impact

### Before Fixes
- ❌ gcloud CLI authentication: **Completely broken** (401/403 errors)
- ❌ OpenAI CLI authentication: **Completely broken** (404 invalid model errors)
- ❌ Users forced to use API keys, defeating the purpose of CLI auth

### After Fixes
- ✅ gcloud CLI authentication: **Works correctly** with OAuth bearer tokens
- ✅ OpenAI CLI authentication: **Works correctly** with normalized model IDs
- ✅ API key fallback: **Still works** for all providers
- ✅ OpenRouter: **Unaffected**, continues to use vendor-prefixed model IDs

---

## Security Considerations

### Bearer Token Handling
- Bearer tokens are now properly isolated from API keys
- No token leakage through incorrect headers
- Tokens only used with appropriate authorization mechanism

### Model ID Normalization
- No security implications
- Purely a compatibility fix
- Doesn't expose any sensitive information

---

## Acknowledgments

Bugs identified by: **chatgpt-codex-connector** bot in PR review #3438350228

Fixed using TDD methodology to ensure:
- Bugs are reproducible
- Fixes are verified
- Regressions are prevented
- Edge cases are covered

---

## Related Issues

- PR Review: https://github.com/Bafff/llm-council/pull/2#pullrequestreview-3438350228
- Original PR: https://github.com/Bafff/llm-council/pull/2

## Version

- **Fixed in**: Next release (after PR merge)
- **Severity**: Critical (breaks CLI authentication entirely)
- **Priority**: High

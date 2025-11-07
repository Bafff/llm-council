# 🔑 API Keys & Model Versions Guide

## 📚 Where to Find Latest Model Versions

### Gemini (Google)
**Latest Models Page**: https://ai.google.dev/gemini-api/docs/models

**Current Latest** (as of 2025-01-07):
- `gemini-2.5-flash` - Fastest, free tier available
- `gemini-2.5-pro` - Most capable, state-of-the-art thinking model

### Claude (Anthropic)
**Models Page**: https://docs.anthropic.com/en/docs/about-claude/models

**Current Latest**:
- `claude-sonnet-4-5-20250514` - Latest Sonnet 4.5

### OpenRouter (GPT-4, Grok, etc)
**Models Page**: https://openrouter.ai/models

**Popular Models**:
- `openai/gpt-4-turbo` - GPT-4 Turbo
- `x-ai/grok-beta` - Grok from xAI

---

## 🆓 Free API Keys

### 1. Gemini (Google) - **FREE!**

**Get Key**: https://aistudio.google.com/apikey

**Setup Steps**:
1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Select or create a Google Cloud project
4. **IMPORTANT**: Enable "Generative Language API" in Google Cloud Console
   - Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
   - Click "Enable"
5. Copy your API key
6. Set environment variable:
   ```bash
   export GOOGLE_API_KEY="your_key_here"
   ```

**Limits**:
- 60 requests per minute (free tier)
- 1,500 requests per day (free tier)

**Common Issues**:
- **403 Forbidden**: API not enabled in Google Cloud Console
  - Solution: Enable "Generative Language API" at https://console.cloud.google.com/apis/library
- **404 Not Found**: Wrong model name
  - Solution: Check current models at https://ai.google.dev/gemini-api/docs/models

### 2. Claude (Anthropic) - **$5 free credit**

**Get Key**: https://console.anthropic.com/

**Setup**:
1. Sign up at https://console.anthropic.com/
2. Get $5 free credit for testing
3. Create API key in settings
4. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your_key_here"
   ```

**Pricing** (after free credit):
- Input: $3 per million tokens
- Output: $15 per million tokens

### 3. OpenRouter - **Pay as you go (cheap)**

**Get Key**: https://openrouter.ai/

**Why OpenRouter?**:
- Access to GPT-4, Grok, and 100+ other models
- Much cheaper than direct APIs
- Single API key for all models

**Setup**:
1. Sign up at https://openrouter.ai/
2. Add $5-10 credit
3. Create API key
4. Set environment variable:
   ```bash
   export OPENROUTER_API_KEY="your_key_here"
   ```

**Pricing Examples**:
- GPT-4 Turbo: $0.01/1K tokens (10x cheaper than OpenAI)
- Grok: $5/1M tokens

---

## 🔧 Configuration in LLM Council

### Set API Keys

**Option 1: Environment Variables** (recommended)
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GOOGLE_API_KEY="AIzaSy..."
export OPENROUTER_API_KEY="sk-or-..."
```

**Option 2: .env File**
```bash
cd llm_council
nano .env
```

Add:
```env
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIzaSy...
OPENROUTER_API_KEY=sk-or-...
```

**Option 3: Interactive Setup**
```bash
llm-council setup
```

### Check Available Models
```bash
llm-council models
```

### Test Single Model
```bash
llm-council ask "Test" --hide-individual
```

---

## 🎯 Recommended Setup

**For Testing** (Free):
1. Gemini (FREE) - 60 req/min
2. Claude ($5 credit) - High quality

**For Production** (Paid):
1. Claude (Anthropic) - Best quality
2. GPT-4 via OpenRouter - Good alternative
3. Gemini - Fast, cheap fallback

---

## ⚠️ Troubleshooting

### Gemini 403 Forbidden

**Problem**: `403 POST https://generativelanguage.googleapis.com/...`

**Solutions**:
1. Enable API in Google Cloud Console:
   - Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
   - Click "Enable" button
   - Wait 1-2 minutes for activation

2. Check API key restrictions:
   - Go to: https://console.cloud.google.com/apis/credentials
   - Click on your API key
   - Remove any IP or referrer restrictions for testing

3. Verify project has billing enabled (even for free tier):
   - Go to: https://console.cloud.google.com/billing
   - Link a billing account (won't be charged for free tier)

### Claude Rate Limit

**Problem**: `429 Too Many Requests`

**Solutions**:
- Wait 60 seconds
- Reduce request frequency
- Upgrade to paid tier for higher limits

### OpenRouter Invalid Key

**Problem**: `401 Unauthorized`

**Solutions**:
- Verify API key is correct
- Check account has credits
- Regenerate API key if needed

---

## 📊 Model Comparison

| Model | Speed | Quality | Cost (per 1M tokens) | Free Tier |
|-------|-------|---------|---------------------|-----------|
| Gemini 2.5 Flash | ⚡⚡⚡ Fast | 🌟🌟🌟 Good | $0 | ✅ 60/min |
| Gemini 2.5 Pro | ⚡⚡ Medium | 🌟🌟🌟🌟 Excellent | ~$7 | ✅ 15/min |
| Claude Sonnet 4.5 | ⚡⚡ Medium | 🌟🌟🌟🌟🌟 Best | $3-15 | ✅ $5 credit |
| GPT-4 Turbo | ⚡ Slow | 🌟🌟🌟🌟 Excellent | $10-30 | ❌ |
| Grok | ⚡⚡ Medium | 🌟🌟🌟 Good | $5 | ❌ |

---

## 🔗 Useful Links

- **LLM Council Docs**: README.md
- **Quick Start**: QUICKSTART.md
- **Commands Cheatsheet**: COMMANDS.md
- **Update Guide**: UPDATE_GUIDE.md

- **Gemini Models**: https://ai.google.dev/gemini-api/docs/models
- **Claude Models**: https://docs.anthropic.com/en/docs/about-claude/models
- **OpenRouter Models**: https://openrouter.ai/models

- **Gemini API Keys**: https://aistudio.google.com/apikey
- **Claude API Keys**: https://console.anthropic.com/
- **OpenRouter API Keys**: https://openrouter.ai/

---

**Last Updated**: 2025-01-07
**Gemini SDK Version**: google-genai >= 0.2.0 (new SDK, 2025)

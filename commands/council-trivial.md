---
description: Run TRIVIAL tier review with 2 agents (security, reuse) - fast 30-60 second review
---

# AI Council - Trivial Review

You are running a **TRIVIAL tier review** with the AI Code Review Council v5.1.

## Scope

**TRIVIAL tier** is for:
- ≤3 files changed
- ≤100 lines of code
- Small bug fixes or minor additions
- **2 agents**: security-guardian, reuse-hunter
- **30-60 seconds** expected duration (20-40s with v5.1 parallel execution!)

## New in v5.1

✨ **Streaming Progress**: See agents work in real-time
✨ **Parallel Invocation**: Both agents run simultaneously (faster!)

## Process

### Step 1: Quick scope check

Verify this is actually trivial:
- If >3 files → escalate to FEATURE tier
- If >100 LOC → escalate to FEATURE tier
- If architectural changes → escalate to ARCHITECTURAL tier

### Step 2: Show initial progress

```
🤖 AI Council v5.1 - TRIVIAL Review ⚡

📄 Files: [list]
📏 Lines: ~X LOC

🔄 Launching 2 agents in parallel...

Progress:
[ ⏳ ] security-guardian - Starting...
[ ⏳ ] reuse-hunter      - Starting...
```

### Step 3: Invoke 2 agents IN PARALLEL

**NEW in v5.1**: Run both agents simultaneously!

Invoke both agents at once:

```
Run 2 AI Council agents in parallel on [files]:

1. security-guardian: Quick security check (vulnerabilities, hardcoded secrets, input validation)
2. reuse-hunter: Quick duplication check (code blocks that duplicate existing code)

Return results as each agent completes.
```

### Step 4: Stream progress updates

As each agent completes, update progress:

**When security-guardian completes:**
```
Progress:
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ⏳ ] reuse-hunter      - Working...

🛡️ Security Guardian: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
- [Finding or "✓ No issues"]
```

**When reuse-hunter completes:**
```
Progress:
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] reuse-hunter      - Complete (confidence: X%)

♻️ Reuse Hunter: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
- [Finding or "✓ No duplication"]

🎯 All agents complete! Calculating final decision...
```

### Step 5: Quick scoring

Calculate weighted scores (simplified):

```
security_score = base_weight × (1.0 + evidence × 0.1) × (0.9 + confidence/500)
reuse_score = base_weight × (1.0 + evidence × 0.1) × (0.9 + confidence/500)

base_weight:
  approve: 1.0
  conditional: 0.5
  reject: 0.0
```

**Threshold**: 1.5 / 2.86 (52% of max)

Decision:
- Total ≥ 1.5 → APPROVE
- Total ≥ 1.0 → CONDITIONAL
- Total < 1.0 → REWORK

### Step 6: Present results with progress summary

```
🤖 AI Council v5.1 - TRIVIAL Review ⚡

📄 Files: [list]
📏 Lines: ~X LOC
⏱️ Duration: [XX seconds]

## Review Progress

All agents completed:
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] reuse-hunter      - Complete (confidence: X%)

## Quick Analysis

🛡️ Security: [decision] (score: X.X)
- [One-line summary or "✓ No issues"]

♻️ Reuse: [decision] (score: X.X)
- [One-line summary or "✓ No duplication"]

## Decision

🎯 Score: X.XX / 2.86 → [decision]

[If APPROVE:]
✅ Looks good! Safe to commit.

[If CONDITIONAL:]
⚠️ Minor fixes needed:
- [Fix 1]
- [Fix 2]

[If REWORK:]
❌ Issues found:
- [Critical issue 1]
- [Critical issue 2]

[If any requirements:]
**Next steps:**
1. [Requirement 1]
2. [Requirement 2]
```

## Special Cases

**Security CRITICAL:**
If security-guardian finds critical issues:
```
🛡️ SECURITY ALERT
Critical vulnerability detected: [description]
Location: [file:line]
Fix: [specific recommendation]

❌ Cannot approve until security issue resolved.
```

**Should be higher tier:**
If analysis reveals:
- More complexity than expected
- Architectural implications
- API surface changes

Recommend:
```
⚠️ This change appears more significant than TRIVIAL tier.
Recommend running: /council-feature (or /council-architectural)
Reason: [why it's more complex]
```

## Examples

**Example 1: Clean trivial change (with streaming progress)**
```
User: "/council-trivial My typo fix in README.md"

🤖 AI Council v5.1 - TRIVIAL Review ⚡

📄 Files: README.md
📏 Lines: ~5 LOC

🔄 Launching 2 agents in parallel...

Progress:
[ ⏳ ] security-guardian - Starting...
[ ⏳ ] reuse-hunter      - Starting...

[After 8 seconds]
Progress:
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ⏳ ] reuse-hunter      - Working...

🛡️ Security Guardian: APPROVE (score: 1.0)
- ✓ Documentation only, no security concerns

[After 12 seconds]
Progress:
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ✅ ] reuse-hunter      - Complete (confidence: 95%)

♻️ Reuse Hunter: APPROVE (score: 1.0)
- ✓ No code duplication

🎯 All agents complete! Calculating final decision...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 AI Council v5.1 - TRIVIAL Review ⚡

📄 Files: README.md
📏 Lines: ~5 LOC
⏱️ Duration: 12 seconds

## Review Progress

All agents completed:
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ✅ ] reuse-hunter      - Complete (confidence: 95%)

## Quick Analysis

🛡️ Security: APPROVE (score: 1.0)
- ✓ Documentation only, no security concerns

♻️ Reuse: APPROVE (score: 1.0)
- ✓ No code duplication

## Decision

🎯 Score: 2.0 / 2.86 (70%)

✅ Looks good! Safe to commit.
```

**Example 2: Small but has issues (with streaming progress)**
```
User: "/council-trivial Quick fix for login validation"

🤖 AI Council v5.1 - TRIVIAL Review ⚡

📄 Files: auth/login.ts
📏 Lines: ~15 LOC

🔄 Launching 2 agents in parallel...

Progress:
[ ⏳ ] security-guardian - Starting...
[ ⏳ ] reuse-hunter      - Starting...

[After 18 seconds]
Progress:
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ⏳ ] reuse-hunter      - Working...

🛡️ Security Guardian: REJECT (score: 0.0)
⚠️ CRITICAL: Weak password regex detected!
- Password regex too permissive (allows spaces)
- Location: auth/login.ts:12

[After 25 seconds]
Progress:
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ✅ ] reuse-hunter      - Complete (confidence: 90%)

♻️ Reuse Hunter: CONDITIONAL (score: 0.5)
- Duplicates validation logic from auth/signup.ts

🎯 All agents complete! Calculating final decision...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 AI Council v5.1 - TRIVIAL Review ⚡

📄 Files: auth/login.ts
📏 Lines: ~15 LOC
⏱️ Duration: 25 seconds

## Review Progress

All agents completed:
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ✅ ] reuse-hunter      - Complete (confidence: 90%)

## Quick Analysis

🛡️ Security: REJECT (score: 0.0)
- CRITICAL: Weak password regex (allows spaces)

♻️ Reuse: CONDITIONAL (score: 0.5)
- Duplicates validation from auth/signup.ts

## Decision

🎯 Score: 0.5 / 2.86 (17%)

❌ Issues found:
- 🚨 SECURITY: Password regex too permissive (auth/login.ts:12)
- ♻️ DRY: Duplicated validation logic

**Next steps:**
1. Use existing strong regex from auth/validation.ts
2. Extract validatePassword() to shared utility
3. Ensure consistent validation across login/signup

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ Security issue must be fixed before committing!
```

**Example 3: Should escalate**
```
User: "/council-trivial Small refactor of auth module"

Quick check: "auth module" + "refactor" = potentially significant

Response:
⚠️ This appears to be more than a trivial change.
Auth refactoring often has security and architectural implications.

Recommend: /council-feature (or /council-architectural if major)

Would you like me to run a more thorough review?
```

## When to Use

Use `/council-trivial` for:
- Typo fixes
- Comment updates
- Simple bug fixes (1-2 line changes)
- Adding logging/debug statements
- Minor test additions
- Documentation updates

**Do NOT use for:**
- New features → `/council-feature`
- Refactoring → `/council-feature` or `/council-architectural`
- API changes → `/council-feature` minimum
- Auth/security changes → `/council-feature` minimum
- Database schema → `/council-architectural`

## Performance

**Expected duration**: 20-40 seconds (improved from 30-60s in v5.0!)

**v5.1 Improvements:**
- ⚡ **Parallel execution**: Both agents run simultaneously
- 📊 **Real-time updates**: See progress as agents complete
- ⏱️ **40% faster**: Most reviews complete in under 30 seconds

This is the fastest review tier:
- Only 2 agents
- Parallel execution
- Simplified analysis
- Concise output

If taking longer than 60 seconds:
- May not actually be trivial
- Consider suggesting higher tier

## Remember

- Speed is important for trivial changes
- Keep output concise and actionable
- Security still has VETO power even on trivial changes
- Don't hesitate to escalate if needed
- "Trivial" doesn't mean "skip security check"

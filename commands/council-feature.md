---
description: Run FEATURE tier review with 4 agents (security, reuse, API, evolution) - 60-120 seconds
---

# AI Council - Feature Review

You are running a **FEATURE tier review** with the AI Code Review Council v5.1.

## Scope

**FEATURE tier** is for:
- 4-15 files changed
- 100-500 lines of code
- New features or moderate refactoring
- **4 agents**: reuse-hunter, security-guardian, api-sentinel, evolution-guardian
- **NO synthesizer** (you synthesize manually)
- **60-120 seconds** expected duration

## New in v5.1

✨ **Streaming Progress**: Real-time updates as agents work
✨ **Parallel Invocation**: All 4 agents run simultaneously (faster!)

## Process

### Step 1: Identify what to review

Ask the user (if not specified):
- Which files/modules?
- What feature was added/changed?
- Any specific concerns?

### Step 2: Show Initial Progress

```
🤖 AI Council v5.1 - FEATURE Review

📄 Scope: [files to review]
📏 Scale: [X files, Y lines]

🔄 Launching 4 agents in parallel...

Progress:
[ ⏳ ] reuse-hunter      - Starting...
[ ⏳ ] security-guardian - Starting...
[ ⏳ ] api-sentinel      - Starting...
[ ⏳ ] evolution-guardian - Starting...
```

### Step 3: Invoke 4 agents IN PARALLEL

**NEW in v5.1**: Run all 4 agents simultaneously (they're independent!)

Invoke all agents at once with a single request:

```
Run 4 AI Council agents in parallel on [files]:

1. reuse-hunter: Check for code duplication and reuse opportunities
2. security-guardian: Scan for security vulnerabilities
3. api-sentinel: Analyze API surface changes
4. evolution-guardian: Check architectural alignment and LOC budgets

Return results as each agent completes.
```

### Step 4: Stream Progress Updates

**NEW in v5.1**: Update progress display as each agent completes!

As agents finish their reviews, immediately update the progress display:

**When reuse-hunter completes:**
```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ⏳ ] security-guardian - Working...
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...

♻️ Reuse Hunter: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
- [Key finding 1]
- [Key finding 2]
```

**When security-guardian completes:**
```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...

🛡️ Security Guardian: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
- [Security finding 1]
- [Security finding 2]
```

**When api-sentinel completes:**
```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ⏳ ] evolution-guardian - Working...

📡 API Sentinel: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
- [API finding 1]
- [API finding 2]
```

**When evolution-guardian completes:**
```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Complete (confidence: X%)

🧬 Evolution Guardian: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
- [Architecture finding 1]
- [Architecture finding 2]

🎯 All agents complete! Calculating final decision...
```

### Step 5: Calculate weighted score (manual)

For each agent output, calculate score:

```
score = base_weight × evidence_mult × confidence_mult

base_weight:
  approve: 1.0
  conditional: 0.5
  reject: 0.0

evidence_mult = min(1.3, 1.0 + 0.1 × evidence_count)
confidence_mult = min(1.1, max(0.9, 0.9 + confidence / 500))
```

Sum all 4 scores.

**Threshold**: 2.4 / 4.29 (56% of max)

Decision:
- Total ≥ 2.4 → APPROVE
- Total ≥ 2.0 → CONDITIONAL
- Total < 2.0 → REWORK

### Step 6: Consolidate requirements

Merge requirements from all agents:
- Must-have fixes (from REJECT/CONDITIONAL)
- Recommendations (from APPROVE with notes)
- Priority order

### Step 7: Present final results with complete progress history

```
🤖 AI Council v5.1 - FEATURE Review ✨

📄 Scope: [files reviewed]
📏 Scale: [X files, Y lines]
⏱️ Duration: [XX seconds]

## Review Progress

All agents completed:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Complete (confidence: X%)

## Agent Analysis

♻️ Reuse Hunter (confidence: X%)
Decision: [decision] (score: X.X)
- [Key finding 1]
- [Key finding 2]

🛡️ Security Guardian (confidence: X%)
Decision: [decision] (score: X.X)
- [Security finding 1]
- [Security finding 2]

📡 API Sentinel (confidence: X%)
Decision: [decision] (score: X.X)
- [API finding 1]
- [API finding 2]

🧬 Evolution Guardian (confidence: X%)
Decision: [decision] (score: X.X)
- [Architecture finding 1]
- [Architecture finding 2]

## Final Decision

🎯 Total Score: X.XX / 4.29 (X%)

Decision: ✅ APPROVE | ⚠️ CONDITIONAL | ❌ REWORK

**Requirements:**
1. [Consolidated requirement 1]
2. [Consolidated requirement 2]
3. [Recommendation]

**Summary:**
[Brief explanation of the decision and key points]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If APPROVE:]
✅ Feature approved! Ready to commit.

[If CONDITIONAL:]
⚠️ Conditional approval - address requirements above before committing.

[If REWORK:]
❌ Needs rework - significant issues detected. Address critical items.
```

## Special Cases

**Security VETO:**
If security-guardian finds CRITICAL vulnerabilities:
- Immediately escalate to CRITICAL tier
- Do not proceed with normal scoring
- Flag for immediate attention

**API Breaking Changes:**
If api-sentinel finds breaking changes:
- Highlight prominently
- Suggest migration strategy
- Consider marking as CONDITIONAL even if score is APPROVE

**High Duplication:**
If reuse-hunter finds >10% new duplication:
- Must address before approval
- Suggest refactoring approach

## Examples

**Example 1: Clean feature (with streaming progress)**
```
User: "/council-feature Review my new user profile component"

🤖 AI Council v5.1 - FEATURE Review ✨

📄 Scope: components/UserProfile.tsx, hooks/useProfile.ts
📏 Scale: 3 files, 180 lines

🔄 Launching 4 agents in parallel...

Progress:
[ ⏳ ] reuse-hunter      - Starting...
[ ⏳ ] security-guardian - Starting...
[ ⏳ ] api-sentinel      - Starting...
[ ⏳ ] evolution-guardian - Starting...

[After 15 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 90%)
[ ⏳ ] security-guardian - Working...
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...

♻️ Reuse Hunter: APPROVE (score: 0.95)
- No code duplication detected
- Good use of existing useQuery hook

[After 25 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 90%)
[ ✅ ] security-guardian - Complete (confidence: 95%)
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...

🛡️ Security Guardian: APPROVE (score: 1.0)
- Proper input validation on all user fields
- XSS prevention via sanitization

[After 35 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 90%)
[ ✅ ] security-guardian - Complete (confidence: 95%)
[ ✅ ] api-sentinel      - Complete (confidence: 85%)
[ ⏳ ] evolution-guardian - Working...

📡 API Sentinel: APPROVE (score: 0.9)
- 2 new exports: UserProfile, useProfile
- Both well-documented with JSDoc

[After 45 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 90%)
[ ✅ ] security-guardian - Complete (confidence: 95%)
[ ✅ ] api-sentinel      - Complete (confidence: 85%)
[ ✅ ] evolution-guardian - Complete (confidence: 80%)

🧬 Evolution Guardian: APPROVE (score: 0.85)
- 180 LOC within budget (≤500)
- Clean component architecture

🎯 All agents complete! Calculating final decision...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 AI Council v5.1 - FEATURE Review ✨

📄 Scope: components/UserProfile.tsx, hooks/useProfile.ts
📏 Scale: 3 files, 180 lines
⏱️ Duration: 45 seconds

## Review Progress

All agents completed:
[ ✅ ] reuse-hunter      - Complete (confidence: 90%)
[ ✅ ] security-guardian - Complete (confidence: 95%)
[ ✅ ] api-sentinel      - Complete (confidence: 85%)
[ ✅ ] evolution-guardian - Complete (confidence: 80%)

## Final Decision

🎯 Total Score: 3.70 / 4.29 (86%)

Decision: ✅ APPROVE

**Recommendations:**
1. Add integration tests (optional)
2. Consider memoization for profile data (performance)

**Summary:**
High-quality feature implementation with proper security, no duplication,
and clean architecture. Ready to commit!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Feature approved! Ready to commit.
```

**Example 2: Needs fixes (with streaming progress)**
```
User: "/council-feature Check the payment processing changes"

🤖 AI Council v5.1 - FEATURE Review ✨

📄 Scope: services/payment.ts, api/checkout.ts
📏 Scale: 5 files, 320 lines

🔄 Launching 4 agents in parallel...

Progress:
[ ⏳ ] reuse-hunter      - Starting...
[ ⏳ ] security-guardian - Starting...
[ ⏳ ] api-sentinel      - Starting...
[ ⏳ ] evolution-guardian - Starting...

[After 20 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 85%)
[ ⏳ ] security-guardian - Working...
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...

♻️ Reuse Hunter: CONDITIONAL (score: 0.4)
- Duplicated error handling in 3 locations
- Suggest extracting to shared utility

[After 30 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 85%)
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...

🛡️ Security Guardian: REJECT (score: 0.0)
⚠️ CRITICAL VULNERABILITY DETECTED!
- Hardcoded API key at payment.ts:45
- This is a CRITICAL security issue!

[After 40 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 85%)
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ✅ ] api-sentinel      - Complete (confidence: 90%)
[ ⏳ ] evolution-guardian - Working...

📡 API Sentinel: CONDITIONAL (score: 0.5)
- Breaking change: removed processPaymentV1 without deprecation
- Need migration path for existing clients

[After 55 seconds]
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: 85%)
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ✅ ] api-sentinel      - Complete (confidence: 90%)
[ ✅ ] evolution-guardian - Complete (confidence: 88%)

🧬 Evolution Guardian: APPROVE (score: 0.9)
- 320 LOC within budget (≤500)
- Good architecture, clear separation

🎯 All agents complete! Calculating final decision...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤖 AI Council v5.1 - FEATURE Review ✨

📄 Scope: services/payment.ts, api/checkout.ts
📏 Scale: 5 files, 320 lines
⏱️ Duration: 55 seconds

## Review Progress

All agents completed:
[ ✅ ] reuse-hunter      - Complete (confidence: 85%)
[ ✅ ] security-guardian - Complete (confidence: 100%)
[ ✅ ] api-sentinel      - Complete (confidence: 90%)
[ ✅ ] evolution-guardian - Complete (confidence: 88%)

## Final Decision

🎯 Total Score: 1.80 / 4.29 (42%)

Decision: ❌ REWORK

**Critical Issues:**
1. 🚨 SECURITY: Remove hardcoded API key from payment.ts:45
   - Use environment variables instead
   - Rotate the exposed key immediately!

2. ⚠️ API: Deprecate old method before removing
   - Add @deprecated tag to processPaymentV1
   - Provide migration guide

3. ♻️ DRY: Extract error handling to shared utility
   - services/utils/errorHandler.ts
   - Reduces 45 lines of duplication

**Summary:**
Critical security vulnerability must be fixed before proceeding.
API breaking change needs deprecation path. Code duplication should
be addressed for maintainability.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Needs rework - significant issues detected. Address critical items.
```

## When to Use

Use `/council-feature` when:
- Adding new functionality
- Moderate refactoring (100-500 LOC)
- 4-15 files changed
- Not architectural (use `/council-architectural`)
- Not trivial (use `/council-trivial`)

## Performance

Expected duration: **60-120 seconds** (improved from 90-150s in v5.0!)

**v5.1 Improvements:**
- ⚡ **Parallel execution**: All 4 agents run simultaneously
- 📊 **Real-time updates**: See progress as agents complete
- ⏱️ **30% faster**: Typical reviews complete in 45-75 seconds

Factors affecting speed:
- Number of files to analyze
- Complexity of changes
- Agent response times
- Parallel processing capability

If taking longer than 2 minutes, inform user: "Comprehensive analysis in progress..."

## Remember

- You synthesize (no synthesizer agent for FEATURE tier)
- Focus on practical, actionable feedback
- Weighted scoring ensures quality over quantity
- Security always has VETO power
- Clear, concise output preferred

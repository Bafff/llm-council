---
description: View detailed history of AI Council decisions and ADRs
---

# AI Council - History

You are displaying the **decision history** of AI Code Review Council v5.0.

## What to Display

### 1. Header

```
📜 AI Council v5.0 - Decision History

Decision storage: ~/.claude/ai-council/decisions/
```

### 2. Filter Options (if user specifies)

User can request:
- All decisions: `/council-history`
- Specific tier: `/council-history architectural`
- Recent count: `/council-history last 20`
- Date range: `/council-history since 2025-10-01`

### 3. Decision List

Show decisions in reverse chronological order (newest first):

```
## Decisions

[For each decision:]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 YYYY-MM-DD HH:MM | [TIER] | [decision]

**Topic**: [Description or file names]

**Scope**:
- Files: X files changed
- Lines: ~X LOC
- Duration: ~X minutes/seconds

**Agents**:
[For each agent involved:]
- ♻️ Reuse: [decision] (score: X.X) - [brief finding]
- 🛡️ Security: [decision] (score: X.X) - [brief finding]
- 📡 API: [decision] (score: X.X) - [brief finding]
- 🧬 Evolution: [decision] (score: X.X) - [brief finding]
[If ARCHITECTURAL:]
- 🎯 Synthesizer: [final decision]

**Final Score**: X.XX / Y.YY (XX%)

**Decision**: ✅ APPROVED | ⚠️ CONDITIONAL | ❌ REWORK | 🔺 ESCALATED

**Key Requirements**:
1. [Requirement 1]
2. [Requirement 2]

[If ARCHITECTURAL tier:]
**ADR**: [path/to/adr.md]

[If conflicts occurred:]
**Conflicts Resolved**:
- [Agent A] vs [Agent B]: [brief resolution]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. Summary Statistics

At the end, show aggregate stats:

```
## Summary

Total decisions shown: X

By tier:
- TRIVIAL: X (XX%)
- FEATURE: X (XX%)
- ARCHITECTURAL: X (XX%)

By outcome:
- ✅ APPROVED: X (XX%)
- ⚠️ CONDITIONAL: X (XX%)
- ❌ REWORK: X (XX%)
- 🔺 ESCALATED: X (XX%)

Average scores:
- TRIVIAL: X.XX / 2.86 (XX%)
- FEATURE: X.XX / 4.29 (XX%)
- ARCHITECTURAL: X.XX / 7.15 (XX%)
```

### 5. Quick Actions

```
## Actions

- View dashboard: /council-dashboard
- New review: /council [description]
- Configuration: /council-config
- Open ADR: [show command to open specific ADR]
```

## How to Generate History

1. **Scan decision directories**:
   ```
   ~/.claude/ai-council/decisions/architectural/*.md
   ~/.claude/ai-council/decisions/feature/*.md
   ~/.claude/ai-council/decisions/trivial/*.md
   ```

2. **Parse each decision file** (if they exist):
   - Extract metadata from frontmatter or structured content
   - Parse agent decisions
   - Extract scores and requirements

3. **Sort by date** (newest first)

4. **Apply filters** if user specified

5. **Format for display**

## Example: No History

```
📜 AI Council v5.0 - Decision History

## No Decisions Yet

No reviews have been run yet.

## Get Started

Run your first review:
  /council [files or description]

Or use specific tier:
  /council-trivial      - Quick review
  /council-feature      - Feature review
  /council-architectural - Full architectural review

After running reviews, you'll see them here!

## What You'll See

Each decision entry includes:
- Date and time
- Tier and scope
- Agent analyses
- Final decision
- Requirements
- ADRs (for architectural reviews)
```

## Example: History with Entries

```
📜 AI Council v5.0 - Decision History

Showing last 10 decisions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 2025-10-08 14:30 | ARCHITECTURAL | ✅ APPROVED

**Topic**: Auth service refactoring

**Scope**:
- Files: 12 files changed
- Lines: ~650 LOC
- Duration: ~5 minutes

**Agents**:
- ♻️ Reuse: CONDITIONAL (0.5) - Found 45 lines duplicated
- 🛡️ Security: APPROVE (1.0) - No vulnerabilities
- 📡 API: CONDITIONAL (0.7) - Keep old API @deprecated
- 🧬 Evolution: APPROVE (0.9) - Excellent architecture
- 🎯 Synthesizer: APPROVED

**Final Score**: 3.1 / 7.15 (43%)

**Decision**: ✅ APPROVED (with conditions)

**Key Requirements**:
1. Extract shared logic to auth/shared/utils.ts
2. Mark old API methods @deprecated
3. Add new improved API methods
4. Both APIs work for 6 months migration period

**Conflicts Resolved**:
- API Sentinel (initially REJECT) vs Evolution (APPROVE)
- Resolution: Backward compatibility strategy accepted

**ADR**: ~/.claude/ai-council/decisions/architectural/2025-10-08-auth-refactor.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 2025-10-08 11:15 | FEATURE | ⚠️ CONDITIONAL

**Topic**: User profile component

**Scope**:
- Files: 5 files changed
- Lines: ~230 LOC
- Duration: ~90 seconds

**Agents**:
- ♻️ Reuse: APPROVE (0.95) - No duplication
- 🛡️ Security: APPROVE (1.0) - Proper input validation
- 📡 API: CONDITIONAL (0.5) - Missing JSDoc for exports
- 🧬 Evolution: APPROVE (0.85) - Clean architecture

**Final Score**: 2.5 / 4.29 (58%)

**Decision**: ⚠️ CONDITIONAL

**Key Requirements**:
1. Add JSDoc comments for public exports
2. Add integration tests (recommended)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 2025-10-08 09:20 | TRIVIAL | ✅ APPROVED

**Topic**: Fix typo in README

**Scope**:
- Files: 1 file
- Lines: ~5 LOC
- Duration: ~30 seconds

**Agents**:
- 🛡️ Security: APPROVE (1.0) - Documentation only
- ♻️ Reuse: APPROVE (1.0) - No code duplication

**Final Score**: 2.0 / 2.86 (70%)

**Decision**: ✅ APPROVED

**Key Requirements**: None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Summary

Total decisions shown: 10

By tier:
- TRIVIAL: 3 (30%)
- FEATURE: 5 (50%)
- ARCHITECTURAL: 2 (20%)

By outcome:
- ✅ APPROVED: 6 (60%)
- ⚠️ CONDITIONAL: 3 (30%)
- ❌ REWORK: 1 (10%)

## Actions

- Full dashboard: /council-dashboard
- New review: /council [description]
- Filter: /council-history architectural
```

## Special Filters

### By tier
```
User: "/council-history architectural"

Show only ARCHITECTURAL tier decisions
```

### By date
```
User: "/council-history since 2025-10-01"

Show decisions from Oct 1, 2025 onwards
```

### Last N
```
User: "/council-history last 20"

Show last 20 decisions (default is 10)
```

### By decision type
```
User: "/council-history approved"

Show only approved decisions
```

## Notes

- Always show newest first (reverse chronological)
- Keep each entry concise but informative
- Show enough detail to understand the decision
- Include paths to ADRs for reference
- Format consistently
- If no decisions, show helpful getting-started message

## Remember

This is a read-only view of history. The goal is to:
1. Show what decisions were made
2. Provide context for each decision
3. Show patterns over time
4. Help learn from past reviews
5. Make ADRs easy to find

Don't invent data - only show actual decision files that exist.

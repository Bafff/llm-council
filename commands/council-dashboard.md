---
description: View AI Council metrics, review history, and decision statistics
---

# AI Council - Dashboard

You are displaying the **metrics and statistics** for AI Code Review Council v5.0.

## What to Display

### 1. Header

```
📊 AI Council v5.0 - Dashboard

Last updated: [current date/time]
Decision storage: ~/.claude/ai-council/decisions/
```

### 2. Recent Activity

Check for decision files and show recent reviews:

```
## Recent Reviews (Last 10)

[For each recent decision:]
📅 YYYY-MM-DD HH:MM - [TIER] - [decision]
   Topic: [brief description]
   Score: X.XX / Y.YY
   Files: [count] files, ~X LOC
   Duration: ~X minutes
   → [path/to/decision.md]

[Examples:]
📅 2025-10-08 14:30 - ARCHITECTURAL - APPROVED
   Topic: Auth service refactoring
   Score: 3.2 / 7.15
   Files: 12 files, ~650 LOC
   Duration: ~5 minutes
   → ~/.claude/ai-council/decisions/architectural/2025-10-08-auth-refactor.md

📅 2025-10-08 11:15 - FEATURE - CONDITIONAL
   Topic: User profile component
   Score: 2.5 / 4.29
   Files: 5 files, ~230 LOC
   Duration: ~90 seconds
   → ~/.claude/ai-council/decisions/feature/2025-10-08-user-profile.md

[If no history:]
ℹ️  No reviews in history yet. Run /council to start!
```

### 3. Statistics (if history exists)

```
## Review Statistics

**Total Reviews**: X
  - TRIVIAL: X (XX%)
  - FEATURE: X (XX%)
  - ARCHITECTURAL: X (XX%)

**Decisions Breakdown**:
  - ✅ APPROVED: X (XX%)
  - ⚠️ CONDITIONAL: X (XX%)
  - ❌ REWORK: X (XX%)
  - 🔺 ESCALATED: X (XX%)

**Average Scores by Tier**:
  - TRIVIAL: X.XX / 2.86 (XX%)
  - FEATURE: X.XX / 4.29 (XX%)
  - ARCHITECTURAL: X.XX / 7.15 (XX%)
```

### 4. Agent Performance

```
## Agent Activity

♻️ Reuse Hunter
   Reviews participated: X
   Average score: X.XX
   Common findings: [most common issues]

🛡️ Security Guardian
   Reviews participated: X
   Average score: X.XX
   VETOs exercised: X
   Critical issues found: X

📡 API Sentinel
   Reviews participated: X
   Average score: X.XX
   Breaking changes detected: X

🧬 Evolution Guardian
   Reviews participated: X
   Average score: X.XX
   Architecture violations: X

🎯 Synthesizer
   Reviews participated: X (ARCHITECTURAL only)
   Conflicts resolved: X
   ADRs generated: X
```

### 5. Common Issues Found

```
## Top Issues Detected

1. [Issue type] - X occurrences
   Most common in: [tier]
   Typical fix: [brief description]

2. [Issue type] - X occurrences
   Most common in: [tier]
   Typical fix: [brief description]

[Examples:]
1. Code duplication - 15 occurrences
   Most common in: FEATURE tier
   Typical fix: Extract to shared utility

2. Hardcoded secrets - 3 occurrences
   Most common in: TRIVIAL tier
   Typical fix: Use environment variables

3. Breaking API changes - 8 occurrences
   Most common in: ARCHITECTURAL tier
   Typical fix: Deprecation strategy
```

### 6. Debate History (if applicable)

```
## Debates and Conflicts

Total debates: X

Recent conflicts resolved:
- [Date] - API vs Evolution: Breaking changes vs Architecture
  Resolution: [brief outcome]

- [Date] - Security vs Evolution: Security fix vs Performance
  Resolution: [brief outcome]
```

### 7. Recommendations

```
## Insights

📈 **Trends**:
- [Observation about recent reviews]
- [Pattern noticed in decisions]

💡 **Recommendations**:
- [Suggestion based on data]
- [Area for improvement]

[Examples:]
📈 **Trends**:
- 40% of FEATURE reviews need duplication fixes
- Security issues mostly in auth-related changes
- ARCHITECTURAL reviews averaging 4.5 minutes

💡 **Recommendations**:
- Consider pre-review duplication check before coding
- Run security scans on auth changes before review
- ARCHITECTURAL reviews are thorough - allow adequate time
```

### 8. Quick Actions

```
## Quick Actions

- New review: /council [description]
- View config: /council-config
- Recent decisions: /council-history
- Specific tier: /council-trivial, /council-feature, /council-architectural
```

## How to Generate Dashboard

1. **Check for decision files**:
   - `~/.claude/ai-council/decisions/architectural/*.md`
   - `~/.claude/ai-council/decisions/feature/*.md`
   - `~/.claude/ai-council/decisions/trivial/*.md`

2. **Parse decision files** (if exist):
   - Extract tier, decision, score, date
   - Count occurrences
   - Calculate statistics

3. **If no history**:
   Show minimal dashboard with instructions

## Example: Empty Dashboard

```
📊 AI Council v5.0 - Dashboard

## Status

No review history yet.

The AI Council is ready to review your code changes!

## Get Started

Run your first review:
  /council [files or description]

Or use tier-specific commands:
  /council-trivial    - Quick review (30-60s)
  /council-feature    - Feature review (60-120s)
  /council-architectural - Full review (3-10min)

## What You'll See

After running reviews, this dashboard will show:
- Recent review history
- Decision statistics
- Agent performance metrics
- Common issues detected
- Trends and recommendations

Run /council-config to see current configuration.
```

## Example: Dashboard with History

```
📊 AI Council v5.0 - Dashboard

Last updated: 2025-10-08 15:45

## Recent Reviews (Last 5)

📅 2025-10-08 14:30 - ARCHITECTURAL - ✅ APPROVED (3.2/7.15)
   Auth service refactoring - 12 files, ~650 LOC

📅 2025-10-08 11:15 - FEATURE - ⚠️ CONDITIONAL (2.5/4.29)
   User profile component - 5 files, ~230 LOC

📅 2025-10-08 09:20 - TRIVIAL - ✅ APPROVED (2.0/2.86)
   Fix typo in README - 1 file, ~5 LOC

📅 2025-10-07 16:40 - FEATURE - ❌ REWORK (1.8/4.29)
   Payment processing - 8 files, ~410 LOC

📅 2025-10-07 14:15 - ARCHITECTURAL - ⚠️ CONDITIONAL (2.9/7.15)
   Database schema migration - 15 files, ~890 LOC

## Statistics

**Total Reviews**: 23
  - TRIVIAL: 8 (35%)
  - FEATURE: 12 (52%)
  - ARCHITECTURAL: 3 (13%)

**Decisions**:
  - ✅ APPROVED: 14 (61%)
  - ⚠️ CONDITIONAL: 7 (30%)
  - ❌ REWORK: 2 (9%)

## Top Issues

1. Code duplication - 8 occurrences
2. API documentation missing - 5 occurrences
3. LOC over budget - 3 occurrences

## Insights

📈 Most reviews pass first time (61% approval rate)
💡 Consider running trivial tier for small changes to save time

## Quick Actions

- New review: /council [description]
- All decisions: /council-history
- Configuration: /council-config
```

## Notes

- If no history, show helpful getting-started info
- Keep statistics simple and visual
- Highlight actionable insights
- Show most recent items first
- Include paths to decision files
- Format dates consistently

## Remember

This is a read-only dashboard. The goal is to:
1. Show review history
2. Provide useful statistics
3. Help users understand patterns
4. Suggest improvements
5. Make next steps clear

Don't invent data - only show what actually exists in decision files.

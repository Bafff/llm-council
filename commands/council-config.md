---
description: Show current AI Council configuration, agents status, and review settings
---

# AI Council - Configuration

You are showing the **configuration and status** of AI Code Review Council v5.0.

## What to Display

### 1. Plugin Information

```
🤖 AI Code Review Council v5.0

**Plugin**: ai-council
**Version**: 5.0.0
**Status**: ✅ Active
**Location**: [plugin installation path]
```

### 2. Agents Status

List all 5 agents and their availability:

```
## Agents

♻️ reuse-hunter
   Status: ✅ Available
   Role: DRY principle enforcer
   Model: Sonnet
   Tools: Read, Grep, Glob, Bash

🛡️ security-guardian
   Status: ✅ Available
   Role: Security vulnerability detector (VETO POWER)
   Model: Sonnet
   Tools: Read, Grep, Glob, Bash

📡 api-sentinel
   Status: ✅ Available
   Role: Public API guardian
   Model: Sonnet
   Tools: Read, Grep, Glob, Bash

🧬 evolution-guardian
   Status: ✅ Available
   Role: Architectural alignment enforcer
   Model: Sonnet
   Tools: Read, Grep, Glob, Bash

🎯 synthesizer
   Status: ✅ Available
   Role: Final decision maker (ARCHITECTURAL tier only)
   Model: Opus
   Tools: Read, Write, Grep, Glob
```

### 3. Review Tiers

```
## Review Tiers

**TRIVIAL** (≤3 files, ≤100 LOC)
  Agents: security-guardian, reuse-hunter (2)
  Threshold: 1.5 / 2.86 (52%)
  Time: 30-60 seconds
  Command: /council-trivial

**FEATURE** (4-15 files, 100-500 LOC)
  Agents: security, reuse, API, evolution (4)
  Threshold: 2.4 / 4.29 (56%)
  Time: 60-120 seconds
  Command: /council-feature

**ARCHITECTURAL** (>15 files, >500 LOC)
  Agents: All 5 (including synthesizer)
  Threshold: 3.0 / 7.15 (42%)
  Time: 3-10 minutes
  Output: ADR (Architecture Decision Record)
  Command: /council-architectural
```

### 4. Scoring Formula

```
## Evidence-Weighted Voting

agent_score = base_weight × evidence_mult × confidence_mult

**Base Weights:**
  approve:     1.0
  conditional: 0.5
  reject:      0.0

**Evidence Multiplier:**
  min(1.3, 1.0 + 0.1 × evidence_count)
  Range: 1.0 to 1.3

**Confidence Multiplier:**
  min(1.1, max(0.9, 0.9 + confidence_percent / 500))
  Range: 0.9 to 1.1

**Maximum possible per agent:** 1.0 × 1.3 × 1.1 = 1.43
```

### 5. Available Commands

```
## Commands

/council                 - Smart review with auto-tier classification
/council-architectural   - Full ARCHITECTURAL tier review
/council-feature         - FEATURE tier review (4 agents)
/council-trivial         - TRIVIAL tier review (2 agents)
/council-config          - Show this configuration
/council-dashboard       - View review history and metrics
/council-history         - View recent council decisions
```

### 6. Configuration Files (if applicable)

Check if project has local configuration:

```
## Local Configuration

[If found:]
✅ Project config: .claude/ai-council/config.yaml
   Mode: [standard|lean|strict]
   Custom thresholds: [yes/no]

[If not found:]
ℹ️  Using default configuration
   To customize: create .claude/ai-council/config.yaml
```

### 7. Decision History Location

```
## Decision Storage

Architectural decisions: ~/.claude/ai-council/decisions/architectural/
Feature decisions: ~/.claude/ai-council/decisions/feature/
Trivial decisions: ~/.claude/ai-council/decisions/trivial/

View recent decisions: /council-history
```

### 8. Special Features

```
## Special Features

🛡️ Security VETO Power
   The security-guardian can escalate any tier to CRITICAL
   if critical vulnerabilities are detected.

🗣️ Debate Protocol
   For ARCHITECTURAL tier, conflicting agents engage in
   evidence-based debates to reach consensus.

📝 ADR Generation
   ARCHITECTURAL tier reviews automatically generate
   Architecture Decision Records for documentation.
```

### 9. Recommendations

Based on current context, provide helpful tips:

```
## Quick Tips

- For small changes: /council-trivial (fastest)
- For new features: /council-feature (balanced)
- For refactoring: /council-architectural (thorough)
- Let /council auto-classify if unsure

- Security issues always require attention
- ADRs are saved for future reference
- All agents have isolated contexts (real independent analysis)
```

## How to Check Status

To determine what to show:

1. **Plugin installed?** - Always yes (this command only works if plugin is active)
2. **Agents available?** - List all 5 agents
3. **Local config?** - Check for `.claude/ai-council/config.yaml`
4. **Recent history?** - Check if decision files exist

## Example Output

```
🤖 AI Code Review Council v5.0

**Plugin**: ai-council
**Version**: 5.0.0
**Status**: ✅ Active

## Agents Status

All 5 agents are available and ready:
♻️ reuse-hunter - DRY principle enforcer
🛡️ security-guardian - Security detector (VETO power)
📡 api-sentinel - Public API guardian
🧬 evolution-guardian - Architecture enforcer
🎯 synthesizer - Final decision maker (Opus)

## Review Tiers

TRIVIAL:       2 agents, 30-60s  → /council-trivial
FEATURE:       4 agents, 60-120s → /council-feature
ARCHITECTURAL: 5 agents, 3-10min → /council-architectural

## Configuration

Mode: Standard (default)
Thresholds: Default
Decision storage: ~/.claude/ai-council/decisions/

## Quick Start

Simple review: /council [files or description]
Let the council auto-classify and analyze your changes!

For specific tier: /council-trivial, /council-feature, /council-architectural
View history: /council-history
```

## Notes

- Keep output organized and easy to scan
- Highlight most useful information
- Provide next steps for the user
- Show real status (don't fake availability)
- Include quick examples of usage

## Remember

This is a status/info command - it's read-only. Just show information clearly and helpfully. The user wants to understand:
1. What's available
2. How to use it
3. What each tier does
4. Where to find more details

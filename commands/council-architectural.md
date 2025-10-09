---
description: Run full ARCHITECTURAL tier review with all 5 agents, debates, and ADR generation
---

# AI Council - Architectural Review

You are running a **full ARCHITECTURAL tier review** with the AI Code Review Council v5.1.

## Scope

This is the most comprehensive review level:
- **All 5 agents** involved (4 analysis + 1 synthesizer)
- **Parallel execution** of analysis agents (faster!)
- **Streaming progress** updates in real-time
- **Debate protocol** if conflicts arise
- **ADR generation** for documentation
- **2-8 minutes** expected duration (improved from 3-10 min!)

## New in v5.1

✨ **Streaming Progress**: Watch all 5 agents work in real-time
✨ **Parallel Invocation**: 4 analysis agents run simultaneously
✨ **Faster Reviews**: 30-40% speed improvement

## Process

### Step 1: Identify scope

Ask the user (if not already specified):
- Which files/modules to review?
- What is the architectural change?
- Are there specific concerns?

### Step 2: Show initial progress

```
🤖 AI Council v5.1 - ARCHITECTURAL Review 🏛️

📄 Scope: [files/modules to review]
📏 Scale: [X files, Y lines]

🔄 Launching 4 analysis agents in parallel...

Progress:
[ ⏳ ] reuse-hunter      - Starting...
[ ⏳ ] security-guardian - Starting...
[ ⏳ ] api-sentinel      - Starting...
[ ⏳ ] evolution-guardian - Starting...
[ 📝 ] synthesizer       - Waiting for analysis agents...
```

### Step 3: Invoke 4 analysis agents IN PARALLEL

**NEW in v5.1**: Run all 4 analysis agents simultaneously!

Invoke all agents at once with a single request:

```
Run 4 AI Council analysis agents in parallel on [files/modules]:

1. reuse-hunter: Analyze for code duplication and reuse opportunities (DRY violations, extractable logic)
2. security-guardian: Scan for security vulnerabilities (SQL injection, XSS, secrets, auth issues)
3. api-sentinel: Analyze API surface changes (breaking changes, backward compatibility)
4. evolution-guardian: Check architectural alignment (LOC budgets, patterns, code health)

Return detailed results as each agent completes.
```

### Step 4: Stream progress updates

As each analysis agent completes, update progress and show findings:

**When first agent completes (example: reuse-hunter):**
```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ⏳ ] security-guardian - Working...
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...
[ 📝 ] synthesizer       - Waiting for analysis agents...

♻️ Reuse Hunter: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
Evidence:
- [Finding 1 with file:line]
- [Finding 2 with file:line]
```

**When second agent completes:**
```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ⏳ ] api-sentinel      - Working...
[ ⏳ ] evolution-guardian - Working...
[ 📝 ] synthesizer       - Waiting for analysis agents...

🛡️ Security Guardian: [APPROVE|CONDITIONAL|REJECT] (score: X.X)
Evidence:
- [Security finding 1 with CWE if applicable]
- [Security finding 2]
```

**Continue for all 4 agents...**

**When all 4 analysis agents complete:**
```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Complete (confidence: X%)
[ ⏳ ] synthesizer       - Starting synthesis...

🎯 All analysis agents complete! Checking for conflicts...
```

### Step 5: Detect conflicts

Compare agent decisions:
- If 2+ agents have opposite decisions (APPROVE vs REJECT), there's a conflict
- If scores vary widely (0.3 vs 0.9), investigate

### Step 6: Run debate round (if conflicts detected)

If conflicts were detected in Step 5:

```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Complete (confidence: X%)
[ 🔄 ] synthesizer       - Debate in progress...

⚠️ CONFLICT DETECTED - Initiating debate protocol...

Conflicting agents: [Agent X] vs [Agent Y]
- [Agent X]: [decision] - [key reasoning]
- [Agent Y]: [opposite decision] - [key reasoning]
```

For conflicting agents, re-invoke with context:

```
"Agent X said [decision] because [reasoning].
Agent Y said [opposite decision] because [reasoning].
Please reconsider your analysis in light of Agent Y's evidence."
```

Allow agents to revise their positions, then update progress:

```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Revised (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Revised (confidence: X%)
[ ⏳ ] synthesizer       - Starting synthesis...

✅ Debate complete - conflicts resolved
```

### Step 7: Invoke synthesizer

**Critical**: Only invoke synthesizer AFTER all 4 analysis agents have completed (and debate if needed).

```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Complete (confidence: X%)
[ ⏳ ] synthesizer       - Synthesizing final decision...
```

Invoke synthesizer with all agent results:

```
"You are the Synthesizer for AI Council v5.1.

Here are the 4 agent analyses:

**Reuse Hunter:**
- Decision: [decision]
- Confidence: [X%]
- Evidence: [key points]
- Requirements: [list]

**Security Guardian:**
- Decision: [decision]
- Confidence: [X%]
- Evidence: [key points]
- Requirements: [list]

**API Sentinel:**
- Decision: [decision]
- Confidence: [X%]
- Evidence: [key points]
- Requirements: [list]

**Evolution Guardian:**
- Decision: [decision]
- Confidence: [X%]
- Evidence: [key points]
- Requirements: [list]

[If debate occurred:]
**Debate Results:**
- [Agent] revised position: [new decision] - [reasoning]
- [Agent] revised position: [new decision] - [reasoning]

Please:
1. Calculate weighted scores using Council v5.0 formula
2. Resolve any remaining conflicts
3. Make final decision (APPROVE/CONDITIONAL/ESCALATE)
4. Generate implementation strategy
5. List all requirements
6. Create Architecture Decision Record (ADR)
"
```

When synthesizer completes:

```
Progress:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Complete (confidence: X%)
[ ✅ ] synthesizer       - Complete!

🎯 All 5 agents complete! Generating final report...
```

### Step 8: Present comprehensive results with full progress history

```
🤖 AI Council v5.1 - ARCHITECTURAL Review 🏛️

📄 Scope: [files/modules reviewed]
📏 Scale: [X files, Y lines]
⏱️ Duration: [X minutes Y seconds]

## Review Progress

All agents completed:
[ ✅ ] reuse-hunter      - Complete (confidence: X%)
[ ✅ ] security-guardian - Complete (confidence: X%)
[ ✅ ] api-sentinel      - Complete (confidence: X%)
[ ✅ ] evolution-guardian - Complete (confidence: X%)
[ ✅ ] synthesizer       - Complete!

## Round 1: Agent Analysis

♻️ Reuse Hunter (confidence: X%)
Decision: [decision] (score: X.X)
Evidence:
- [Finding 1 with file:line]
- [Finding 2 with file:line]
Requirements:
- [Requirement 1]

🛡️ Security Guardian (confidence: X%)
Decision: [decision] (score: X.X)
Evidence:
- [Finding 1 - CWE if applicable]
- [Finding 2]
Requirements:
- [Requirement 1]

📡 API Sentinel (confidence: X%)
Decision: [decision] (score: X.X)
Evidence:
- [Breaking changes detected]
- [API surface analysis]
Requirements:
- [Requirement 1]

🧬 Evolution Guardian (confidence: X%)
Decision: [decision] (score: X.X)
Evidence:
- [Architecture findings]
- [LOC analysis]
Requirements:
- [Requirement 1]

[If conflicts:]
⚠️ CONFLICT DETECTED
- Security: REJECT - [critical vulnerability found]
- Evolution: APPROVE - [excellent architecture]

## Round 2: Debate

🛡️ Security Guardian (revised, confidence: X%)
Decision: CONDITIONAL (score: X.X)
- After seeing Evolution's architecture benefits
- Recommend: [specific security fix]
- Then can approve

🧬 Evolution Guardian (revised, confidence: X%)
Decision: APPROVE (score: X.X)
- Security's fix is architecturally acceptable
- Maintains design quality

## Synthesizer Decision

🎯 Final Score: X.XX / 7.15 ✅ APPROVED (CONDITIONAL)

**Strategy:**
1. [Implement recommendation 1]
2. [Implement recommendation 2]
3. [Migration approach]

**Requirements:**
1. [Consolidated requirement from agents]
2. [Additional requirement from synthesis]
3. [Testing requirements]

**Implementation Notes:**
- [Key consideration 1]
- [Key consideration 2]

## Proposed Refactoring

[If applicable, show refactored code structure]

Files changed:
- src/module1.ts (refactored, -120 LOC)
- src/shared/utils.ts (new, +80 LOC)
- tests/module1.test.ts (updated)

## Architecture Decision Record

📝 ADR saved to: ~/.claude/ai-council/decisions/architectural/YYYY-MM-DD-[topic].md

**Decision**: [APPROVE/CONDITIONAL/ESCALATE]
**Context**: [What prompted this architectural change]
**Consequences**: [Trade-offs and implications]
**Migration**: [How to safely implement]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Would you like to:
[a] Proceed with this refactoring
[b] Show me the proposed code changes
[c] Modify something specific
[d] Reject and keep original
```

### Step 9: Save ADR

Create the ADR file at `~/.claude/ai-council/decisions/architectural/YYYY-MM-DD-[topic].md`:

```markdown
# Architecture Decision Record: [Title]

**Date**: YYYY-MM-DD
**Status**: [Approved/Conditional/Rejected]
**Tier**: ARCHITECTURAL

## Context

[What architectural problem are we solving?]

## Decision

[What did we decide to do?]

## Rationale

### Agent Analysis

**Reuse Hunter**: [summary]
**Security Guardian**: [summary]
**API Sentinel**: [summary]
**Evolution Guardian**: [summary]

### Weighted Scores

- Reuse: X.XX
- Security: X.XX
- API: X.XX
- Evolution: X.XX
- **Total**: X.XX / 7.15

### Conflicts Resolved

[If any conflicts occurred, how were they resolved?]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Trade-off 1]
- [Trade-off 2]

## Implementation

### Requirements
1. [Requirement 1]
2. [Requirement 2]

### Migration Strategy
[Step-by-step approach]

### Timeline
[Estimated effort]

## Alternatives Considered

[What other options were evaluated?]

## References

[Links to related decisions, documentation, issues]
```

## Notes

**v5.1 Performance:**
- **Parallel execution** of 4 analysis agents significantly reduces time
- **Streaming progress** keeps user informed in real-time
- Average review time: 2-5 minutes (down from 3-10 minutes!)
- Synthesizer still runs sequentially (needs all agent inputs)

**Best Practices:**
- This is the most thorough review - allow adequate time
- Progress updates show automatically as agents complete
- Debate rounds (if needed) add 1-2 minutes
- Save ADR even if decision is REJECT (document why)
- For very large changes (>20 files), consider breaking into smaller reviews

## When to Use

Use this command when:
- Refactoring major modules (>500 LOC)
- Changing core architecture
- Major API redesigns
- Cross-cutting concerns
- User explicitly requests architectural review
- Changes affect >15 files

## Remember

You are the orchestrator. The agents do the analysis. Your job:
1. Invoke them in the right order
2. Collect their insights
3. Facilitate debates if needed
4. Let synthesizer make final call
5. Document the decision thoroughly

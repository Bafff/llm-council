---
description: Create comprehensive refactoring plan with multi-agent analysis and debate
---

# 🔨 AI Council - Refactoring Plan Generator

You are orchestrating a **comprehensive refactoring analysis** using AI Council's specialized refactoring agents.

## 🎯 Mission

Generate a detailed, actionable refactoring plan for large, monolithic files through:
1. **Multi-agent parallel analysis** (Round 1)
2. **Cross-agent debate and refinement** (Round 2)
3. **Synthesis into actionable plan** (Final Output)

---

## 📋 Input

**Required Parameter:**
- `<file_path>` - Path to the file to analyze for refactoring

**Optional Parameters:**
- `--mode=full` - Full analysis (default)
- `--mode=quick` - Skip debate round, faster
- `--output=<path>` - Custom output location

**Example:**
```
/ai-council:council-refactor-plan theme_details.html
/ai-council:council-refactor-plan src/dashboard.jsx --mode=full
/ai-council:council-refactor-plan legacy/monolith.js --output=docs/refactor-plan.md
```

---

## 🤖 Agent Lineup

You will launch 5 specialized refactoring agents:

1. **🏗️ Architecture Analyst** - Identifies components and boundaries
2. **🔗 Dependency Mapper** - Maps all dependencies and coupling
3. **⚠️ Risk Assessor** - Evaluates risks and mitigation strategies
4. **🎨 UX Continuity Guardian** - Protects user experience
5. **📊 Complexity Analyzer** - Measures complexity and estimates effort

---

## 📈 Execution Protocol

### Step 1: Initial Context (5 seconds)

Show user what's about to happen:

```
🔨 AI Council v5.1 - Refactoring Plan Generator

📄 Target File: theme_details.html
📏 Analyzing large monolithic file for refactoring opportunities...

🤖 Launching 5 specialized agents:
   🏗️ Architecture Analyst
   🔗 Dependency Mapper
   ⚠️ Risk Assessor
   🎨 UX Continuity Guardian
   📊 Complexity Analyzer

⏱️ Expected Duration: 10-15 minutes
💾 Output will be saved to: ~/.claude/ai-council/refactoring-plans/

---
```

### Step 2: Show Streaming Progress

Display real-time agent status:

```
🔄 Round 1: Multi-Agent Analysis (5-10 min)

Progress:
[ ⏳ ] 🏗️ Architecture Analyst     - Starting analysis...
[ ⏳ ] 🔗 Dependency Mapper        - Starting analysis...
[ ⏳ ] ⚠️ Risk Assessor            - Starting analysis...
[ ⏳ ] 🎨 UX Continuity Guardian   - Starting analysis...
[ ⏳ ] 📊 Complexity Analyzer      - Starting analysis...
```

Update as agents complete:

```
[ ✅ ] 🏗️ Architecture Analyst     - Complete! (12 components identified)
[ ✅ ] 🔗 Dependency Mapper        - Complete! (45 dependencies mapped)
[ ⏳ ] ⚠️ Risk Assessor            - Working... (3 critical risks found)
[ ⏳ ] 🎨 UX Continuity Guardian   - Working... (5 workflows analyzed)
[ ⏳ ] 📊 Complexity Analyzer      - Working... (calculating metrics)
```

### Step 3: Launch Round 1 Agents (PARALLEL)

**IMPORTANT:** Launch ALL 5 agents in a SINGLE message using multiple Task tool calls!

Invoke all agents simultaneously:

```markdown
Task 1: Architecture Analyst
- subagent_type: "ai-council:refactoring:Architecture Analyst"
- description: "Analyze architecture for refactoring"
- prompt: "You are the Architecture Analyst for AI Council's Refactoring Planning.

Analyze this file for refactoring: [FILE_PATH]

Follow all protocols in the agent instructions.

Save your analysis to: /tmp/refactor_architecture.md

Be comprehensive. Identify all components. Provide clear boundaries."
```

```markdown
Task 2: Dependency Mapper
- subagent_type: "ai-council:refactoring:Dependency Mapper"
- description: "Map dependencies for refactoring"
- prompt: "You are the Dependency Mapper for AI Council's Refactoring Planning.

Analyze this file: [FILE_PATH]

Follow all protocols in the agent instructions.

Save your analysis to: /tmp/refactor_dependencies.md

Map every dependency. Identify circular dependencies. Recommend decoupling."
```

```markdown
Task 3: Risk Assessor
- subagent_type: "ai-council:refactoring:Risk Assessor"
- description: "Assess refactoring risks"
- prompt: "You are the Risk Assessor for AI Council's Refactoring Planning.

First, read the outputs from other agents:
- Architecture: /tmp/refactor_architecture.md
- Dependencies: /tmp/refactor_dependencies.md

Then analyze risks for: [FILE_PATH]

Follow all protocols in the agent instructions.

Save your analysis to: /tmp/refactor_risks.md

Identify all risks. Provide mitigation strategies. Calculate risk scores."
```

```markdown
Task 4: UX Continuity Guardian
- subagent_type: "ai-council:refactoring:UX Continuity Guardian"
- description: "Ensure UX preservation"
- prompt: "You are the UX Continuity Guardian for AI Council's Refactoring Planning.

Analyze this file: [FILE_PATH]

Follow all protocols in the agent instructions.

Save your analysis to: /tmp/refactor_ux.md

Map all user workflows. Identify UX-critical code. Define test requirements."
```

```markdown
Task 5: Complexity Analyzer
- subagent_type: "ai-council:refactoring:Complexity Analyzer"
- description: "Analyze complexity and estimate effort"
- prompt: "You are the Complexity Analyzer for AI Council's Refactoring Planning.

First, read outputs from other agents:
- Architecture: /tmp/refactor_architecture.md
- Dependencies: /tmp/refactor_dependencies.md
- Risks: /tmp/refactor_risks.md

Then analyze: [FILE_PATH]

Follow all protocols in the agent instructions.

Save your analysis to: /tmp/refactor_complexity.md

Measure all complexity metrics. Estimate effort. Calculate ROI."
```

### Step 4: Round 1 Complete

After all agents finish:

```
🎯 Round 1 Complete! (8 minutes elapsed)

Key Findings:
🏗️ Architecture: 12 components identified, 3 phases proposed
🔗 Dependencies: 45 dependencies, 2 circular loops found
⚠️ Risks: 8 risks identified (3 critical, 5 medium)
🎨 UX Impact: 5 user workflows affected, test plan created
📊 Complexity: MI=42 (poor) → MI=79 (good), ROI 178%

---
```

### Step 5: Debate & Refinement (if --mode=full)

Show debate progress:

```
🔄 Round 2: Cross-Agent Debate (3-5 min)

Agents are discussing:
• Architecture Analyst proposes extracting ThemeModal
• Risk Assessor warns: high risk due to event handler complexity
• Dependency Mapper confirms: circular dependency with ThemeCard
• UX Guardian adds: modal animations must be preserved
• Complexity Analyzer suggests: defer to Phase 3, focus on low-risk first

Reaching consensus...
```

Launch debate agents sequentially (they need to read each other's outputs):

```markdown
Task 6: Architecture Analyst (Debate)
- prompt: "Read all agent outputs from /tmp/refactor_*.md

Review the concerns from:
- Risk Assessor (risks identified)
- Dependency Mapper (coupling issues)
- UX Guardian (UX preservation requirements)
- Complexity Analyzer (effort estimates)

Refine your component boundaries and extraction order based on their feedback.

Save refined analysis to: /tmp/refactor_architecture_v2.md"
```

[Similar for other agents if significant disagreements found]

### Step 6: Synthesis

Create final refactoring plan:

```
🎯 Synthesizing Final Refactoring Plan...

Combining insights from all agents:
✅ Component boundaries validated
✅ Dependencies analyzed
✅ Risks mitigated
✅ UX preserved
✅ Effort estimated

Generating comprehensive refactoring plan...
```

### Step 7: Read All Agent Outputs

Use Read tool to gather all analyses:

```bash
cat /tmp/refactor_architecture.md
cat /tmp/refactor_dependencies.md
cat /tmp/refactor_risks.md
cat /tmp/refactor_ux.md
cat /tmp/refactor_complexity.md
```

If debate happened:
```bash
cat /tmp/refactor_architecture_v2.md  # Refined versions
```

### Step 8: Generate Final Plan

Create comprehensive document combining all insights:

**Output Structure:**

```markdown
# Refactoring Plan: [FILE_NAME]

**Generated:** [DATE]
**AI Council Version:** 5.1.0
**Analysis Duration:** [X] minutes
**Agents Consulted:** 5 (Architecture, Dependencies, Risks, UX, Complexity)

---

## Executive Summary

**File:** [FILE_PATH]
**Current State:** [LOC] lines, Maintainability Index [XX], [X] critical issues
**Proposed State:** [LOC] lines across [N] components, MI [XX], issues resolved
**Effort Estimate:** [XX] hours ([X] weeks)
**ROI:** [XX]% in year 1
**Recommendation:** PROCEED / PROCEED WITH CAUTION / DO NOT PROCEED

**Top 3 Priorities:**
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

---

## 1. Architecture Analysis

[Paste Architecture Analyst's output]

### Components Identified

[Component list with boundaries]

### Extraction Order

[Phase-by-phase plan]

---

## 2. Dependency Analysis

[Paste Dependency Mapper's output]

### Dependency Graph

[Visual representation]

### Circular Dependencies

[Loops and how to break them]

### Decoupling Strategies

[Specific recommendations]

---

## 3. Risk Assessment

[Paste Risk Assessor's output]

### Critical Risks

[Top risks with mitigation]

### Rollback Plan

[How to undo if needed]

### Success Criteria

[What "done" looks like]

---

## 4. UX Continuity Plan

[Paste UX Guardian's output]

### User Workflows Affected

[Workflows with test requirements]

### Visual Regression Tests

[Screenshot list]

### Accessibility Requirements

[A11y checklist]

---

## 5. Complexity & Effort Analysis

[Paste Complexity Analyzer's output]

### Current vs Proposed Complexity

[Metrics comparison table]

### Effort Breakdown

[Phase-by-phase hours]

### Cost-Benefit Analysis

[ROI calculation]

---

## 6. Integrated Refactoring Roadmap

### Week 0: Preparation (30 hours)

**Tasks:**
- [ ] Write missing tests ([X] tests needed)
- [ ] Set up visual regression baseline
- [ ] Configure error monitoring
- [ ] Document current state

**Deliverables:**
- Test coverage report
- Performance baseline
- Visual regression baseline
- Risk mitigation checklist

---

### Week 1: Low-Risk Extractions (Phase 1)

**Components:**
1. [Component A] - [X] hours
2. [Component B] - [X] hours

**Testing:**
- [ ] Unit tests for each component
- [ ] Integration tests for interactions
- [ ] Visual regression check

**Risks:**
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]

**Success Metrics:**
- All tests passing
- No visual regressions
- Performance within 10% of baseline

---

### Week 2: Medium-Risk Extractions (Phase 2)

[Similar structure]

---

### Week 3-4: High-Risk Extractions (Phase 3)

[Similar structure]

---

## 7. Testing Strategy

### Pre-Refactoring Tests (Must Write)

**Unit Tests:**
- [ ] [Test 1]
- [ ] [Test 2]

**Integration Tests:**
- [ ] [Test 1]
- [ ] [Test 2]

**E2E Tests:**
- [ ] [Workflow 1]
- [ ] [Workflow 2]

### During Refactoring (Continuous)

- Daily: Run full test suite
- End of each phase: Manual QA
- Weekly: Visual regression check

### Post-Refactoring (Validation)

- Performance audit
- Accessibility audit
- User acceptance testing

---

## 8. Rollback Procedures

### Trigger Conditions

Rollback if:
- [Condition 1]
- [Condition 2]

### Rollback Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]

---

## 9. Decision Summary

### Go/No-Go Recommendation

**Recommendation:** [PROCEED / CAUTION / DO NOT PROCEED]

**Rationale:**
[Synthesized reasoning from all agents]

**Conditions for Proceeding:**
1. [Condition 1]
2. [Condition 2]
3. [Condition 3]

**If Conditions Not Met:**
[Alternative approach]

---

## 10. Agent Consensus

### Agreement Areas

✅ All agents agree:
- [Agreement 1]
- [Agreement 2]

### Debate Points

⚠️ Agents debated:
- **Issue:** [Description]
- **Positions:**
  - Architecture Analyst: [Position]
  - Risk Assessor: [Position]
- **Resolution:** [How it was resolved]

### Confidence Levels

| Agent | Confidence | Key Uncertainties |
|-------|------------|-------------------|
| Architecture Analyst | XX% | [Uncertainty] |
| Dependency Mapper | XX% | [Uncertainty] |
| Risk Assessor | XX% | [Uncertainty] |
| UX Guardian | XX% | [Uncertainty] |
| Complexity Analyzer | XX% | [Uncertainty] |

---

## 11. Next Steps

### Immediate Actions (Today)

1. [ ] [Action 1]
2. [ ] [Action 2]

### This Week

1. [ ] [Action 1]
2. [ ] [Action 2]

### Before Starting Refactoring

1. [ ] [Prerequisite 1]
2. [ ] [Prerequisite 2]

---

## 12. Appendices

### Appendix A: Agent Detailed Outputs

- Architecture Analysis: /tmp/refactor_architecture.md
- Dependency Analysis: /tmp/refactor_dependencies.md
- Risk Assessment: /tmp/refactor_risks.md
- UX Analysis: /tmp/refactor_ux.md
- Complexity Analysis: /tmp/refactor_complexity.md

### Appendix B: References

- AI Council v5.1 Documentation
- Refactoring Agent Templates
- Best Practices for Large-Scale Refactoring

---

**Generated by:** AI Council v5.1 Refactoring Planning System
**Agents Involved:** 5 specialized refactoring agents
**Total Analysis Time:** [XX] minutes
**Plan Version:** 1.0
**Review Status:** Ready for team review

---

**Next Step:** Share this plan with your team and get approval before proceeding!
```

### Step 9: Save Output

Save the final plan to:

```
~/.claude/ai-council/refactoring-plans/[filename]-refactoring-plan-[timestamp].md
```

Example:
```
~/.claude/ai-council/refactoring-plans/theme_details-refactoring-plan-20251009-143022.md
```

### Step 10: Summary for User

Show concise summary:

```
✅ Refactoring Plan Complete! (12 minutes total)

📄 Plan saved to:
~/.claude/ai-council/refactoring-plans/theme_details-refactoring-plan-20251009-143022.md

📊 Key Findings:

Components: 12 identified
Phases: 3 (Low → Medium → High risk)
Effort: 134 hours (3.3 weeks)
ROI: 178% in year 1
Risks: 8 identified, 3 critical (all mitigated)

🎯 Recommendation: PROCEED WITH CAUTION

✅ Proceed if:
  1. Write 30 missing tests first
  2. Set up visual regression baseline
  3. Allocate 4 weeks (with buffer)

🔧 Next Steps:
  1. Review plan with team
  2. Get stakeholder approval
  3. Write pre-refactoring tests (Week 0)
  4. Start Phase 1 extractions

📖 Full plan: [path to saved file]

---

Want to start refactoring now? Use:
  /ai-council:council-refactor-execute [component-name]

Want to create custom agents? Use:
  /ai-council:council-agent-create
```

---

## ⚙️ Configuration

### Default Settings

```yaml
refactoring:
  mode: full                    # full | quick
  output_dir: ~/.claude/ai-council/refactoring-plans/
  include_debate: true          # Round 2 debate
  save_intermediate: true       # Save /tmp/refactor_*.md files
  streaming_progress: true      # Show real-time updates
```

### Customization

Users can override in `~/.claude/ai-council/agents-config.yaml`:

```yaml
refactoring_config:
  mode: quick                   # Skip debate for faster analysis
  min_file_size: 500            # Only analyze files > 500 LOC
  output_format: markdown       # markdown | json | html
```

---

## 🚨 Edge Cases

### File Too Small

If file < 300 LOC:

```
⚠️ File is only [XXX] lines.

Refactoring may not be necessary for files this small.

Recommendations:
- If code is complex: Proceed with analysis
- If code is simple: Consider skipping refactoring
- Threshold: 300+ LOC typically benefits from refactoring

Continue anyway? (y/n)
```

### File Not Found

```
❌ Error: File not found: [FILE_PATH]

Please check:
- File path is correct
- File exists in the repository
- You have read permissions

Usage: /ai-council:council-refactor-plan <file_path>
```

### Agent Failure

If any agent fails:

```
⚠️ Agent [AGENT_NAME] failed to complete analysis.

Error: [ERROR_MESSAGE]

Options:
1. Retry agent
2. Continue without this agent (reduced accuracy)
3. Abort analysis

What would you like to do?
```

---

## 📚 Examples

### Example 1: Large HTML File

```
/ai-council:council-refactor-plan src/dashboard.html

Output:
- 15 components identified
- 3 circular dependencies
- 8 critical risks
- 180 hours effort
- ROI: 215%
- Recommendation: PROCEED
```

### Example 2: Monolithic JavaScript

```
/ai-council:council-refactor-plan legacy/app.js --mode=full

Output:
- 8 modules identified
- 12 god functions found
- Complexity: MI 35 → 82
- 95 hours effort
- ROI: 165%
- Recommendation: PROCEED WITH CAUTION
```

### Example 3: Quick Analysis

```
/ai-council:council-refactor-plan utils/helpers.js --mode=quick

Output:
- Skipped debate round
- 6 minutes total (vs 12 minutes full)
- 4 utility groups identified
- 20 hours effort
- Recommendation: PROCEED
```

---

## 🎯 Success Criteria

This command succeeds if:

✅ All 5 agents complete analysis
✅ Final plan is comprehensive (> 1000 words)
✅ Actionable recommendations provided
✅ Risk mitigation strategies included
✅ Effort estimates realistic
✅ ROI calculation included
✅ Plan saved to file system
✅ User has clear next steps

---

## 💡 Tips for Users

**Before running:**
- Commit your changes (plan may be saved in repo)
- Ensure file is > 300 LOC (smaller files may not need refactoring)
- Have 15 minutes available (analysis takes time)

**During analysis:**
- Watch streaming progress to see what agents find
- Don't interrupt (agents run in parallel)

**After completion:**
- Review plan with your team
- Discuss risks and mitigation strategies
- Get stakeholder approval
- Follow the roadmap phases

**Best practices:**
- Run on largest, most problematic files first
- Use `--mode=quick` for initial exploration
- Use `--mode=full` for production refactoring decisions
- Save plan to docs/ folder for team reference

---

**Command Version:** 1.0
**AI Council Version:** 5.1.0
**Agent Count:** 5 specialized refactoring agents
**Expected Duration:** 10-15 minutes (full mode), 6-8 minutes (quick mode)

🎉 **Good luck with your refactoring!**

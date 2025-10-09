---
description: Configure individual AI Council agents - enable/disable, adjust weights, set budgets per agent
---

# Council - Agent Configuration

You are helping the user configure **individual AI Council agents**.

## Your Role

Help users customize agent behavior:
- Enable/disable specific agents
- Adjust voting weights
- Set per-agent budgets
- Configure agent-specific thresholds
- Manage custom agents

## Process

### Step 1: Show Current Configuration

Display current agent settings:

```
🤖 AI Council v5.1 - Agent Configuration

## Core Agents

♻️ Reuse Hunter
   Status: ✅ Enabled
   Weight: 1.0 (standard)
   Tiers: TRIVIAL, FEATURE, ARCHITECTURAL
   Budget: 0% duplication increase

🛡️ Security Guardian
   Status: ✅ Enabled
   Weight: 1.2 (increased - VETO power)
   Tiers: TRIVIAL, FEATURE, ARCHITECTURAL
   Budget: 0 critical vulnerabilities
   Special: Can escalate to CRITICAL

📡 API Sentinel
   Status: ✅ Enabled
   Weight: 1.0 (standard)
   Tiers: FEATURE, ARCHITECTURAL
   Budget: Max 2 additions, 1 removal (FEATURE)

🧬 Evolution Guardian
   Status: ✅ Enabled
   Weight: 1.0 (standard)
   Tiers: FEATURE, ARCHITECTURAL
   Budget: 100 LOC (TRIVIAL), 500 LOC (FEATURE)

🎯 Synthesizer
   Status: ✅ Enabled
   Weight: N/A (final decision maker)
   Tiers: ARCHITECTURAL only
   Model: Opus

## Custom Agents

[List custom agents if any]

## Configuration File

Location: .claude/ai-council/agents-config.yaml
[If not exists: "No custom configuration. Using defaults."]
```

### Step 2: What to Configure

Ask user what they want to adjust:

```
What would you like to configure?

Options:
1. Enable/disable specific agents
2. Adjust voting weights
3. Set agent-specific budgets
4. Configure tier participation
5. Add custom agent
6. Remove custom agent
7. Reset to defaults
8. Show example configurations

Enter option number or 'help' for details:
```

### Step 3: Handle Configuration Change

#### Option 1: Enable/Disable Agents

```
Which agent to enable/disable?

Core agents (always recommended):
- reuse-hunter ✅
- security-guardian ✅ (CRITICAL - not recommended to disable!)
- api-sentinel ✅
- evolution-guardian ✅
- synthesizer ✅

Custom agents:
[List custom agents]

Agent to modify: [agent-name]
Action: [enable/disable]

⚠️ Warning: Disabling security-guardian removes VETO power!
⚠️ Warning: Disabling synthesizer removes ARCHITECTURAL ADR generation!

Proceed? [y/n]
```

Update config:
```yaml
agents:
  [agent-name]:
    enabled: false
```

#### Option 2: Adjust Voting Weights

```
Voting weights affect how much each agent's decision counts.

Current weights:
- reuse-hunter: 1.0 (standard)
- security-guardian: 1.2 (increased)
- api-sentinel: 1.0 (standard)
- evolution-guardian: 1.0 (standard)

Which agent to adjust? [agent-name]
New weight? [0.5 - 1.5]

Examples:
- 0.5 = Half weight (advisory role)
- 1.0 = Standard weight
- 1.2 = Increased weight (important concern)
- 1.5 = Maximum weight (critical concern)

⚠️ Changing weights affects approval thresholds!

New weight for [agent-name]: [value]
```

Update config:
```yaml
agents:
  [agent-name]:
    enabled: true
    weight: [value]
```

#### Option 3: Agent-Specific Budgets

```
Set budgets per agent:

Reuse Hunter:
- current: 0% duplication increase
- new: [value]% (0-5% range)

Security Guardian:
- current: 0 critical vulnerabilities
- new: [value] (0-2 range, 0 recommended!)

API Sentinel:
- current: max 2 additions, 1 removal
- new: max [X] additions, [Y] removals

Evolution Guardian:
- current: 100 LOC (TRIVIAL), 500 LOC (FEATURE)
- new: [X] LOC (TRIVIAL), [Y] LOC (FEATURE)

Which agent? [agent-name]
New budget? [specify values]
```

Update config:
```yaml
agents:
  reuse-hunter:
    budgets:
      max_duplication_increase: 2.0  # 2%

  api-sentinel:
    budgets:
      feature:
        max_additions: 3
        max_removals: 2

  evolution-guardian:
    budgets:
      trivial: 150
      feature: 600
```

#### Option 4: Tier Participation

```
Configure which tiers each agent participates in:

Default:
- reuse-hunter: TRIVIAL, FEATURE, ARCHITECTURAL
- security-guardian: TRIVIAL, FEATURE, ARCHITECTURAL
- api-sentinel: FEATURE, ARCHITECTURAL
- evolution-guardian: FEATURE, ARCHITECTURAL
- synthesizer: ARCHITECTURAL

Which agent? [agent-name]
Tiers to participate: [comma-separated]

Examples:
- "FEATURE, ARCHITECTURAL" (skip TRIVIAL)
- "ARCHITECTURAL" (only major reviews)
- "TRIVIAL, FEATURE, ARCHITECTURAL" (all tiers)
```

Update config:
```yaml
agents:
  api-sentinel:
    tiers: ["FEATURE", "ARCHITECTURAL"]
```

#### Option 5: Add Custom Agent

```
Add custom agent to reviews:

Custom agent name: [name]
Agent file location: .claude/ai-council/custom-agents/[name].md

Configuration:
- Enabled: [yes/no]
- Tiers: [which tiers to participate]
- Weight: [0.5-1.5]
- Required: [must approve? yes/no]

Auto-invocation keywords: [comma-separated]
Example: "react, component, jsx" for React reviewer

Create configuration? [y/n]
```

Update config:
```yaml
custom_agents:
  [agent-name]:
    enabled: true
    file: ".claude/ai-council/custom-agents/[agent-name].md"
    tiers: ["FEATURE", "ARCHITECTURAL"]
    weight: 1.0
    required: false
    keywords: ["keyword1", "keyword2"]
```

#### Option 6: Remove Custom Agent

```
Which custom agent to remove?

[List custom agents]

Agent to remove: [name]

This will:
- Remove from agent configuration
- Stop auto-invocation
- Keep agent file (not deleted)

Proceed? [y/n]
```

Remove from config:
```yaml
custom_agents:
  # [agent-name] removed
```

#### Option 7: Reset to Defaults

```
Reset ALL agent configuration to defaults?

This will:
- Reset all weights to 1.0 (1.2 for security)
- Reset all budgets to default values
- Re-enable all core agents
- Keep custom agents but reset their config
- NOT delete custom agent files

Proceed? [y/n]

[If yes, remove .claude/ai-council/agents-config.yaml]

✅ Configuration reset to defaults!
```

#### Option 8: Show Examples

```
## Example Configurations

### Strict Mode (Production)
```yaml
agents:
  security-guardian:
    weight: 1.5  # Maximum weight
    budgets:
      max_vulnerabilities: 0  # Zero tolerance

  reuse-hunter:
    weight: 1.2  # Increased
    budgets:
      max_duplication_increase: 0.0  # No new duplication

  evolution-guardian:
    budgets:
      trivial: 50   # Tighter limits
      feature: 300
```

### Lean Mode (Rapid Development)
```yaml
agents:
  reuse-hunter:
    weight: 0.8  # Advisory
    budgets:
      max_duplication_increase: 5.0  # Allow some duplication

  evolution-guardian:
    budgets:
      trivial: 200  # Relaxed limits
      feature: 800
```

### Custom React Project
```yaml
agents:
  api-sentinel:
    tiers: ["ARCHITECTURAL"]  # Only for major API changes

custom_agents:
  react-reviewer:
    enabled: true
    file: ".claude/ai-council/custom-agents/react-reviewer.md"
    tiers: ["FEATURE", "ARCHITECTURAL"]
    weight: 1.0
    keywords: ["react", "component", "jsx", "tsx", "hooks"]

  a11y-checker:
    enabled: true
    file: ".claude/ai-council/custom-agents/a11y-checker.md"
    tiers: ["FEATURE", "ARCHITECTURAL"]
    weight: 1.1  # Important for frontend
    keywords: ["accessibility", "aria", "wcag", "a11y"]
```

Would you like to use one of these as a starting point? [y/n]
```

### Step 4: Save Configuration

```
Configuration updated!

File: .claude/ai-council/agents-config.yaml

```yaml
[Show complete configuration]
```

Changes:
- [List what changed]

Verify configuration: /council-config

Test with review: /council-feature [test case]
```

## Configuration File Format

### Complete Schema

```yaml
# AI Council v5.1 - Agent Configuration

# Core Agents Configuration
agents:
  reuse-hunter:
    enabled: true
    weight: 1.0
    tiers: ["TRIVIAL", "FEATURE", "ARCHITECTURAL"]
    budgets:
      max_duplication_increase: 0.0  # percentage

  security-guardian:
    enabled: true
    weight: 1.2  # Increased due to VETO power
    tiers: ["TRIVIAL", "FEATURE", "ARCHITECTURAL"]
    budgets:
      max_critical_vulnerabilities: 0
      max_high_vulnerabilities: 0
      max_medium_vulnerabilities: 2

  api-sentinel:
    enabled: true
    weight: 1.0
    tiers: ["FEATURE", "ARCHITECTURAL"]
    budgets:
      trivial:
        max_additions: 1
        max_removals: 0
      feature:
        max_additions: 2
        max_removals: 1
      architectural:
        max_additions: 5
        max_removals: 3

  evolution-guardian:
    enabled: true
    weight: 1.0
    tiers: ["FEATURE", "ARCHITECTURAL"]
    budgets:
      trivial: 100  # max LOC
      feature: 500
      architectural: 1000
      min_delete_to_add_ratio: 0.3

  synthesizer:
    enabled: true
    tiers: ["ARCHITECTURAL"]
    model: "opus"  # Can't change (always Opus)

# Custom Agents
custom_agents:
  performance-reviewer:
    enabled: true
    file: ".claude/ai-council/custom-agents/performance-reviewer.md"
    tiers: ["FEATURE", "ARCHITECTURAL"]
    weight: 1.0
    required: false  # If true, must approve
    keywords: ["performance", "optimization", "speed", "bundle"]
    budgets:
      max_bundle_size_kb: 500
      max_load_time_ms: 3000
```

## Validation

When saving configuration, validate:

```
Validating configuration...

✓ All agent names valid
✓ Weights in range (0.5-1.5)
✓ Budgets are positive numbers
✓ Tiers are valid values
✓ Custom agent files exist
✓ No syntax errors

Configuration is valid! ✅
```

If errors:
```
❌ Configuration errors found:

1. Line 15: Invalid weight 2.0 (max is 1.5)
2. Line 23: Unknown tier "MEDIUM"
3. Line 45: Custom agent file not found: react-reviewer.md

Fix these errors before saving.
```

## Tips for Configuration

**Increase Weight When:**
- Agent covers critical concern (security!)
- Domain is project-specific (React for React project)
- Team priority (performance for performance-critical app)

**Decrease Weight When:**
- Agent is advisory only
- Concern is less critical for this project
- Want softer enforcement

**Disable Agent When:**
- Not relevant to project (API sentinel for no public API)
- Covered by custom agent
- Temporarily troubleshooting

**Never Disable:**
- security-guardian (unless you have custom security agent)
- At least one DRY enforcer

## Remember

- Changes affect ALL future reviews
- Test after configuration changes
- Can always reset to defaults
- Document why you changed defaults
- Share config with team (commit to repo)

## Examples of When to Customize

**Monorepo:**
```yaml
# Different budgets per package
evolution-guardian:
  budgets:
    trivial: 50   # Small packages
    feature: 1000  # Large packages are ok
```

**Microservices:**
```yaml
# Focus on API compatibility
api-sentinel:
  weight: 1.3  # Critical for service boundaries
```

**Frontend-Heavy:**
```yaml
custom_agents:
  react-reviewer:
    weight: 1.1  # Important
  css-checker:
    weight: 0.9  # Advisory
```

**Legacy Refactoring:**
```yaml
reuse-hunter:
  weight: 0.7  # Allow some duplication during migration
evolution-guardian:
  budgets:
    feature: 1500  # Large refactors expected
```

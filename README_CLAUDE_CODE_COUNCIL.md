# Claude Code Council

**AI-powered multi-agent code review system for Claude Code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blue.svg)](https://github.com/646826/claude-code-council)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/646826/claude-code-council)

Get intelligent, evidence-based code reviews from 5 specialized AI agents working in parallel. Catch security issues, enforce DRY principles, protect your APIs, and maintain architectural consistency—all before you commit.

---

## 🎯 What Does It Do?

Claude Code Council is a **multi-agent code review system** that analyzes your code changes through multiple expert lenses:

- **🛡️ Security Guardian** - Detects vulnerabilities (SQL injection, XSS, exposed secrets)
- **🔍 Reuse Hunter** - Finds code duplication and suggests refactoring
- **🔌 API Sentinel** - Catches breaking changes in public APIs
- **🏗️ Evolution Guardian** - Enforces architectural patterns and budgets
- **⚖️ Synthesizer** - Combines all findings into actionable decisions

Think of it as having 5 expert developers review your code simultaneously, each focusing on their specialty.

---

## ✨ Key Features

### 🔄 Real-Time Streaming Progress
Watch agents work in real-time:
```
🔄 Launching 4 agents in parallel...

Progress:
[ ⏳ ] security-guardian - Scanning for vulnerabilities...
[ ✅ ] reuse-hunter      - Complete! Found 3 duplications
[ ⏳ ] api-sentinel      - Checking public APIs...
[ ⏳ ] evolution-guardian - Validating architecture...
```

### ⚡ 30-50% Faster Reviews
Parallel execution means multiple agents analyze code simultaneously instead of sequentially.

### 🎨 Extensible
Create custom agents for your specific needs:
- React/Vue component reviewers
- Database query optimizers
- Accessibility checkers
- Performance analyzers

---

## 🚀 Quick Start

### Installation

1. **Clone this repository**

```bash
git clone https://github.com/646826/claude-code-council.git
cd claude-code-council
```

2. **Set up as a local marketplace**

```bash
# Create marketplace directory
mkdir -p ~/.claude-marketplaces/local
cp -r . ~/.claude-marketplaces/local/claude-code-council

# Create marketplace.json
cat > ~/.claude-marketplaces/local/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "local-marketplace",
  "owner": {
    "name": "Local User"
  },
  "metadata": {
    "description": "Local Claude Code Council marketplace",
    "version": "1.0.0"
  },
  "plugins": [
    {
      "name": "claude-code-council",
      "source": "./claude-code-council",
      "description": "AI Code Review Council - Multi-agent code review system",
      "version": "1.0.0"
    }
  ]
}
EOF
```

3. **Install in Claude Code**

```bash
cd /your/project
claude
```

In the Claude Code chat:

```
/plugin marketplace add ~/.claude-marketplaces/local
/plugin install claude-code-council@local-marketplace
```

Choose **"Install now"**, then restart Claude Code.

4. **Verify installation**

```
/ai-council:council-config
```

You should see the plugin configuration!

---

## 📖 How to Use

### Basic Commands

All commands use the `ai-council:` namespace. **Tip**: Type `/council` and press **Tab** for autocomplete!

#### Auto-classify and Review

```bash
/ai-council:council
```

The system automatically classifies your changes and runs the appropriate review tier.

#### Quick Review (TRIVIAL tier - 20-40 seconds)

```bash
/ai-council:council-trivial src/utils/validation.ts
```

**Best for:**
- Bug fixes
- Small utility functions
- Minor changes (≤3 files)

**Agents:** Security Guardian + Reuse Hunter

#### Feature Review (FEATURE tier - 45-75 seconds)

```bash
/ai-council:council-feature src/services/
```

**Best for:**
- New features
- Service layer changes
- Multiple file changes (4-15 files)

**Agents:** Security Guardian + Reuse Hunter + API Sentinel + Evolution Guardian

#### Architectural Review (ARCHITECTURAL tier - 2-5 minutes)

```bash
/ai-council:council-architectural
```

**Best for:**
- Major refactoring
- Architecture changes
- Breaking changes (>15 files)

**Agents:** All 5 agents + ADR (Architecture Decision Record) generation

---

## 💡 Real-World Use Cases

### Use Case 1: Before Committing a Feature

**Scenario:** You just added email validation to your user registration

```bash
# Review your changes
/ai-council:council-feature src/auth/

# Output (example):
🤖 AI Council - FEATURE Review ✨

Progress:
[ ✅ ] security-guardian - Complete (95%)
[ ✅ ] reuse-hunter      - Complete (85%)
[ ✅ ] api-sentinel      - Complete (92%)
[ ✅ ] evolution-guardian - Complete (88%)

Decision: ⚠️ CONDITIONAL APPROVAL
Score: 3.1 / 4.29 (72%)

🛡️ Security Findings:
- ⚠️ Email validation uses simple regex - vulnerable to bypass
- ✅ Password hashing is secure (bcrypt with salt)

🔍 Code Duplication:
- ⚠️ Email validation logic duplicated in 2 files:
  - src/auth/register.ts:45
  - src/auth/profile.ts:78
  Suggestion: Extract to src/utils/validators.ts

🔌 API Impact:
- ✅ No breaking changes to public API
- 📝 New endpoint: POST /auth/validate-email (backward compatible)

Requirements before merging:
1. Use industry-standard email regex or library like validator.js
2. Extract duplicate email validation to shared utility
3. Add tests for edge cases (unicode emails, etc.)

Ready to fix? Address the 2 issues above, then commit! ✨
```

**What you learned:**
- Your email validation has security issues
- Code is duplicated
- API changes are safe
- Clear action items to fix before merging

---

### Use Case 2: Refactoring a Monolithic File

**Scenario:** You have a 1,200-line `dashboard.tsx` that's become unmaintainable

```bash
/ai-council:council-refactor-plan src/dashboard.tsx

# Output (example):
🔨 AI Council - Refactoring Plan Generator

📄 Target: src/dashboard.tsx (1,247 lines)

🔄 Launching 5 specialized agents...

Progress:
[ ✅ ] Architecture Analyst     - Complete! (12 components identified)
[ ✅ ] Dependency Mapper        - Complete! (45 dependencies)
[ ✅ ] Risk Assessor            - Complete! (8 risks, 3 critical)
[ ✅ ] UX Continuity Guardian   - Complete! (5 workflows protected)
[ ✅ ] Complexity Analyzer      - Complete! (MI: 42 → 79)

✅ Analysis Complete! (12 minutes)

📊 Key Findings:

Components: 12 identified
├── Phase 1 (Low Risk):  UserProfile, ThemeToggle, Breadcrumbs
├── Phase 2 (Med Risk):  DataTable, FilterPanel, SearchBar
└── Phase 3 (High Risk): ChartWidget, ThemeModal, Layout

Effort: 134 hours (3.3 weeks)
ROI: 178% in year 1
Risks: 8 identified, 3 critical (all mitigated)

🎯 Recommendation: PROCEED WITH CAUTION

✅ Proceed if:
  1. Write 30 missing tests first (coverage: 23% → 85%)
  2. Set up visual regression baseline
  3. Allocate 4 weeks (with buffer for unknowns)

🔧 Next Steps:
  1. Review full plan: ~/.claude/ai-council/refactoring-plans/dashboard-refactoring-plan-20251009.md
  2. Share with team for approval
  3. Start Week 0: Preparation (write tests, baselines)
  4. Begin Phase 1: Low-risk extractions

📖 Full 47-page plan saved with:
- Component extraction order
- Test requirements for each phase
- Risk mitigation strategies
- Rollback procedures
- Week-by-week roadmap
```

**What you learned:**
- Clear breakdown of 12 components to extract
- 3-phase plan from low to high risk
- Need 30 tests before starting
- Realistic timeline: 3.3 weeks
- ROI calculation: 178% in first year

---

### Use Case 3: Catching API Breaking Changes

**Scenario:** You're refactoring an internal function, but it's actually part of your public API

```bash
/ai-council:council-feature src/api/users.ts

# Output (example):
🤖 AI Council - FEATURE Review

Progress:
[ ✅ ] security-guardian - Complete (100%)
[ ✅ ] reuse-hunter      - Complete (95%)
[ ✅ ] api-sentinel      - Complete (70%)
[ ✅ ] evolution-guardian - Complete (92%)

Decision: 🚫 REJECT
Score: 2.1 / 4.29 (49%)

🔌 CRITICAL API ISSUE:

⛔ BREAKING CHANGE DETECTED in src/api/users.ts:

Line 45:
- export function getUser(id: string): Promise<User>
+ export function getUser(id: number): Promise<User>

Impact:
- Function: getUser (PUBLIC API)
- Change: Parameter type changed from string → number
- Severity: BREAKING CHANGE
- Consumers affected: 12 files across 3 packages

This change will break:
1. Frontend app (src/components/UserProfile.tsx)
2. Admin dashboard (admin/src/users/UserList.tsx)
3. Mobile API client (mobile-sdk/src/api.ts)
... and 9 more files

Recommended solutions:
1. Deprecate old signature, add new one:
   getUser(id: string | number): Promise<User>

2. Create new function, mark old as deprecated:
   getUserById(id: number): Promise<User>
   @deprecated Use getUserById instead
   getUser(id: string): Promise<User>

3. Use semver MAJOR bump (v2.0.0) and document migration

Decision: REJECT until breaking change is resolved
This change CANNOT be merged without a deprecation strategy.
```

**What you learned:**
- You were about to break 12 files across 3 packages
- API Sentinel caught this before merge
- Clear migration strategies provided
- Prevented a production incident!

---

### Use Case 4: Security Review Before Deploy

**Scenario:** Final security check before deploying payment processing

```bash
/ai-council:council-trivial src/payments/stripe.ts

# Output (example):
🤖 AI Council - TRIVIAL Review ⚡

Progress:
[ ✅ ] security-guardian - Complete (100%)
[ ✅ ] reuse-hunter      - Complete (92%)

Decision: 🚫 VETO (Security Guardian used VETO power)

🛡️ CRITICAL SECURITY VULNERABILITIES:

⛔ SEVERITY: CRITICAL - Exposed Secret

Line 12:
const stripeKey = "sk_live_abc123def456...";

Issue: Stripe secret key hardcoded in source code
Risk: Key will be committed to Git, exposed in repo
Impact: CRITICAL - Full account access, financial fraud

Required fix:
1. Move to environment variable:
   const stripeKey = process.env.STRIPE_SECRET_KEY;

2. Add to .env (NOT committed):
   STRIPE_SECRET_KEY=sk_live_abc123def456...

3. Add .env to .gitignore

4. Rotate the exposed key immediately:
   https://dashboard.stripe.com/apikeys

---

⛔ SEVERITY: HIGH - SQL Injection Risk

Line 45:
const query = `SELECT * FROM orders WHERE user_id = ${userId}`;

Issue: Direct string interpolation in SQL query
Risk: SQL injection attack
Impact: HIGH - Database breach, data exposure

Required fix:
Use parameterized queries:
const query = 'SELECT * FROM orders WHERE user_id = ?';
db.query(query, [userId]);

---

This code MUST NOT be deployed until these issues are fixed.

Security Guardian has VETOED this change.
```

**What you learned:**
- Caught hardcoded Stripe key before it hit Git
- Found SQL injection vulnerability
- Security Guardian used VETO power (cannot override)
- Prevented a major security incident

---

## 🤖 The Agents Explained

### 1. 🛡️ Security Guardian
**Focus:** Vulnerability detection

**Catches:**
- SQL injection, XSS, CSRF attacks
- Exposed secrets (API keys, passwords)
- Insecure crypto, weak hashing
- Authentication/authorization flaws

**Special power:** VETO - Can block critical security issues

**Example finding:**
```
⛔ SQL Injection in src/users.ts:34
  db.query(`SELECT * FROM users WHERE id = ${id}`)
  Fix: Use parameterized queries
```

---

### 2. 🔍 Reuse Hunter
**Focus:** DRY (Don't Repeat Yourself) principle

**Catches:**
- Code duplication (≥5 lines)
- Similar logic in multiple files
- Reinventing existing utilities

**Suggests:**
- Extract to shared functions
- Use existing libraries
- Create abstractions

**Example finding:**
```
🔍 Duplication detected (12 lines):
  - src/auth/login.ts:45-57
  - src/auth/signup.ts:78-90
  Extract to: src/utils/validators.ts
```

---

### 3. 🔌 API Sentinel
**Focus:** Public API compatibility

**Catches:**
- Breaking changes (removed/renamed exports)
- Parameter type changes
- Return type changes
- Signature modifications

**Tracks:**
- API surface budget
- Semver compliance
- Deprecation policies

**Example finding:**
```
🔌 Breaking change in src/api.ts:
  - export function getUser(id: string)
  + export function getUser(id: number)

  Affects: 12 files across 3 packages
  Suggest: Add overload or deprecate
```

---

### 4. 🏗️ Evolution Guardian
**Focus:** Architectural consistency

**Catches:**
- LOC budget violations (files > 500 lines)
- Pattern inconsistencies
- Layer violations (e.g., UI calling DB directly)
- Missing documentation

**Enforces:**
- Code organization standards
- Codebase health metrics
- Architectural patterns

**Example finding:**
```
🏗️ LOC budget exceeded:
  src/dashboard.tsx: 1,247 lines (budget: 500)

  Suggest: Split into components:
  - DashboardLayout (200 LOC)
  - DataTable (300 LOC)
  - Filters (150 LOC)
```

---

### 5. ⚖️ Synthesizer
**Focus:** Final decision making

**Responsibilities:**
- Combine findings from all agents
- Calculate weighted scores
- Resolve conflicts
- Generate ADRs (architectural tier only)
- Provide actionable recommendations

**Decisions:**
- ✅ APPROVE - Ready to merge
- ⚠️ CONDITIONAL - Fix issues first
- 🚫 REJECT - Major problems, cannot merge

**Example output:**
```
⚖️ Synthesis:

Score: 3.2 / 4.29 (75%)
Decision: ⚠️ CONDITIONAL APPROVAL

Must fix before merge:
1. Security: Use env vars for API keys
2. DRY: Extract duplicate validation logic

Optional improvements:
3. Add tests for edge cases
4. Update API documentation
```

---

## 📊 Review Tiers

### TRIVIAL (20-40 seconds)
**When:** ≤3 files changed, simple fixes

**Agents:** 2 (Security + Reuse)

**Example scenarios:**
- Bug fix in a utility function
- Typo correction
- Small refactoring

**Command:**
```bash
/ai-council:council-trivial src/utils/helpers.ts
```

---

### FEATURE (45-75 seconds)
**When:** 4-15 files, new features

**Agents:** 4 (Security + Reuse + API + Evolution)

**Example scenarios:**
- New API endpoint
- Feature addition
- Service layer changes

**Command:**
```bash
/ai-council:council-feature src/services/
```

---

### ARCHITECTURAL (2-5 minutes)
**When:** >15 files, major changes

**Agents:** 5 (All agents + ADR generation)

**Example scenarios:**
- Large refactoring
- Architecture changes
- Breaking changes
- Database migrations

**Command:**
```bash
/ai-council:council-architectural
```

**Extra output:** Architecture Decision Record (ADR) documenting the changes

---

## 🎨 Creating Custom Agents

Want a React performance reviewer? GraphQL query optimizer? Accessibility checker? Create your own!

### Quick Start

```bash
/ai-council:council-agent-create
```

Interactive wizard walks you through:
1. Choose a template (5 available)
2. Define agent's focus
3. Set review criteria
4. Configure scoring

### Templates Available

**1. Basic Reviewer** - Simple yes/no checks
```markdown
Example: "Does component have PropTypes?"
- Yes → +1 point
- No → -1 point
```

**2. Evidence-Based Reviewer** - Metrics-driven
```markdown
Example: Bundle size analyzer
- < 100KB → +2 points
- 100-200KB → +1 point
- > 200KB → -2 points
```

**3. Specialized Domain** - Tech-specific
```markdown
Example: React best practices
- No inline functions in JSX → +1
- Uses React.memo for heavy components → +1
- Proper key props → +1
```

**4. Budget Tracker** - Enforce limits
```markdown
Example: Performance budgets
- Lighthouse score ≥ 90 → +2
- Bundle size < 200KB → +1
- LOC per component < 300 → +1
```

**5. Hybrid Reviewer** - Multi-concern
```markdown
Example: Full-stack API reviewer
- Security: No secrets in code
- Performance: Response time < 200ms
- Quality: Error handling present
```

### Example: React Performance Agent

```bash
/ai-council:council-agent-create

> Template: specialized-domain
> Name: react-performance-guardian
> Focus: React component performance

Agent created! Now reviews:
✓ Heavy component memoization
✓ Expensive render optimization
✓ useCallback/useMemo usage
✓ Prop drilling vs context
✓ Bundle size impact
```

Now use it:
```bash
/ai-council:council-feature src/components/
# Your custom agent runs automatically!
```

---

## ⚙️ Configuration

### Per-Agent Configuration

Fine-tune agent behavior in `~/.claude/ai-council/agents-config.yaml`:

```yaml
agents:
  security-guardian:
    enabled: true
    weight: 1.5        # Higher priority (default: 1.0)
    tiers: ["TRIVIAL", "FEATURE", "ARCHITECTURAL"]

  reuse-hunter:
    enabled: true
    weight: 1.0
    min_duplication_lines: 5  # Minimum lines to flag as duplicate

  api-sentinel:
    enabled: true
    weight: 1.2
    strict_mode: true  # Flag even minor API changes

custom_agents:
  react-performance-guardian:
    enabled: true
    file: "~/.claude/ai-council/custom-agents/react-perf.md"
    weight: 1.0
    tiers: ["FEATURE", "ARCHITECTURAL"]
```

---

## 🔧 Management Commands

### View Configuration
```bash
/ai-council:council-config
```

Shows:
- Installed agents
- Agent weights
- Tier configuration
- Custom agents

### View Dashboard
```bash
/ai-council:council-dashboard
```

Shows:
- Review history
- Success/rejection rate
- Most common issues
- Agent performance metrics

### View History
```bash
/ai-council:council-history
```

Shows:
- Past reviews
- Decisions made
- ADRs generated
- Trend analysis

### Configure Agents
```bash
/ai-council:council-agent-config
```

Interactive wizard to:
- Enable/disable agents
- Adjust weights
- Set budgets
- Configure tiers

---

## 🚨 Common Issues & Solutions

### "No changes detected"
**Problem:** Council finds no staged changes

**Solution:**
```bash
# Stage your changes first
git add .

# Then run review
/ai-council:council
```

### "Command not found"
**Problem:** Slash command not recognized

**Solution:** Use full namespace:
```bash
/ai-council:council-trivial test.ts
```

Or use Tab autocomplete:
```bash
/council<Tab>
```

### "Agent timeout"
**Problem:** Agent takes too long (>2 minutes)

**Causes:**
- Very large files
- Slow network
- High token usage

**Solution:**
- Review smaller chunks
- Use TRIVIAL tier for quick checks
- Split large files first

---

## 📚 Learn More

- **[Installation Guide](./INSTALLATION.md)** - Detailed setup
- **[Contributing Guide](./CONTRIBUTING.md)** - How to contribute
- **[Agent Templates](./templates/)** - Custom agent examples
- **[Issue Tracker](https://github.com/646826/claude-code-council/issues)** - Report bugs

---

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Code of conduct
- Development setup
- Pull request process
- Creating custom agents

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built for [Claude Code](https://claude.com/claude-code)
- Inspired by multi-agent systems and code review best practices
- Thanks to all contributors!

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/646826/claude-code-council/issues)
- **Discussions**: [GitHub Discussions](https://github.com/646826/claude-code-council/discussions)

---

## 🎯 Roadmap

- [ ] Web dashboard for review history
- [ ] Integration with GitHub Actions
- [ ] Custom agent marketplace
- [ ] Team collaboration features
- [ ] Multi-language support
- [ ] VS Code extension
- [ ] Slack/Discord notifications

---

**Made with ❤️ for the Claude Code community**

**Version**: 1.0.0
**Last Updated**: 2025-10-09

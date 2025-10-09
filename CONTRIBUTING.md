# Contributing to Claude Code Council

Thank you for your interest in contributing to Claude Code Council! This document provides guidelines for contributing to the project.

---

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:

1. **Clear title** - Describe the bug briefly
2. **Steps to reproduce** - How to trigger the bug
3. **Expected behavior** - What should happen
4. **Actual behavior** - What actually happens
5. **Environment** - Claude Code version, OS, etc.
6. **Screenshots** - If applicable

**Example:**

```markdown
## Bug: Security Guardian not detecting XSS in JSX

**Steps to Reproduce:**
1. Run `/ai-council:council-trivial src/Component.jsx`
2. File contains `dangerouslySetInnerHTML`
3. Security Guardian should flag it

**Expected:** Warning about XSS risk
**Actual:** No warning shown

**Environment:**
- Claude Code: v1.2.3
- Plugin: v1.0.0
- OS: macOS 14.0
```

### Suggesting Features

Feature requests are welcome! Please create an issue with:

1. **Problem statement** - What problem does this solve?
2. **Proposed solution** - How should it work?
3. **Alternatives considered** - Other approaches
4. **Use cases** - Real-world examples

---

## 🛠️ Development Setup

### Prerequisites

- Git
- Claude Code (latest version)
- Text editor (VS Code recommended)

### Getting Started

1. **Fork the repository**

```bash
git clone https://github.com/646826/claude-code-council.git
cd claude-code-council
```

2. **Create a development branch**

```bash
git checkout -b feature/your-feature-name
```

3. **Install as local marketplace**

```bash
# Create local marketplace
mkdir -p ~/claude-marketplaces/dev
cp -r . ~/claude-marketplaces/dev/claude-code-council

# Create marketplace.json
cat > ~/claude-marketplaces/dev/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "dev-marketplace",
  "plugins": [
    {
      "name": "claude-code-council",
      "source": "./claude-code-council",
      "version": "dev"
    }
  ]
}
EOF

# Install in Claude Code
claude
/plugin marketplace add ~/claude-marketplaces/dev
/plugin install claude-code-council@dev-marketplace
```

4. **Make your changes**

Edit files in `~/claude-marketplaces/dev/claude-code-council/`

5. **Test your changes**

```bash
# Reinstall plugin
/plugin uninstall claude-code-council@dev-marketplace
/plugin install claude-code-council@dev-marketplace

# Test commands
/ai-council:council-trivial test.ts
```

6. **Commit and push**

```bash
git add .
git commit -m "Add: Your feature description"
git push origin feature/your-feature-name
```

7. **Create a Pull Request**

Go to GitHub and create a PR from your branch.

---

## 📝 Contribution Guidelines

### Code Style

- **Markdown files**: Use consistent formatting
- **Agent files**: Follow the template structure
- **Command files**: Use YAML frontmatter
- **Comments**: Write clear, concise comments

### Agent Development

When creating or modifying agents:

1. **Follow the template structure**

```markdown
---
description: Brief description
---

# Agent Name

## Role
Clear role definition

## Protocols
Step-by-step instructions

## Evidence Collection
How to gather evidence

## Decision Making
How to make decisions

## Output Format
Expected output structure
```

2. **Test with multiple scenarios**

- Simple cases
- Complex cases
- Edge cases
- Error cases

3. **Document your agent**

Add examples and usage notes.

### Command Development

When creating slash commands:

1. **Use YAML frontmatter**

```markdown
---
description: Command description
---
```

2. **Follow the protocol structure**

- Input validation
- Agent invocation
- Progress reporting
- Output formatting

3. **Add error handling**

- File not found
- Invalid parameters
- Agent failures

### Testing

Before submitting a PR:

1. **Test manually**

```bash
# Test all affected commands
/ai-council:council-trivial test.ts
/ai-council:council-feature src/
```

2. **Test edge cases**

- Empty files
- Large files (>1000 LOC)
- Non-code files
- Missing files

3. **Check for errors**

- Review Claude Code output
- Check for warnings
- Verify decisions are correct

---

## 🎨 Creating Custom Agents

### Agent Template

Use the templates in `templates/` as starting points:

```bash
cp templates/basic-reviewer.md agents/my-custom-agent.md
```

### Agent Checklist

- [ ] Clear role definition
- [ ] Step-by-step protocols
- [ ] Evidence collection strategy
- [ ] Decision-making logic
- [ ] Output format specification
- [ ] Example scenarios
- [ ] Error handling

### Registering Your Agent

Add to `.claude-plugin/plugin.json`:

```json
{
  "agents": [
    "./agents/my-custom-agent.md"
  ]
}
```

---

## 📚 Documentation

When adding features, please update:

1. **README.md** - Main documentation
2. **Agent files** - Agent-specific docs
3. **Command files** - Command documentation
4. **Examples** - Usage examples

---

## 🔍 Review Process

### Pull Request Guidelines

1. **Title**: Clear, descriptive title
2. **Description**: What changes and why
3. **Testing**: How you tested
4. **Breaking changes**: List any breaking changes
5. **Screenshots**: If UI/output changes

### Review Criteria

PRs will be reviewed for:

- **Functionality**: Does it work as intended?
- **Code quality**: Is it well-structured?
- **Documentation**: Is it documented?
- **Testing**: Is it tested?
- **Compatibility**: Does it break existing features?

---

## 🚀 Release Process

Releases are managed by maintainers:

1. Version bump in `plugin.json`
2. Update `CHANGELOG.md`
3. Create GitHub release
4. Announce in discussions

---

## 📞 Getting Help

- **Questions**: [GitHub Discussions](https://github.com/646826/claude-code-council/discussions)
- **Issues**: [GitHub Issues](https://github.com/646826/claude-code-council/issues)

---

## 🎯 Good First Issues

Looking for where to start? Check issues labeled:

- `good first issue` - Easy for newcomers
- `help wanted` - Need community help
- `documentation` - Documentation improvements

---

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone.

### Our Standards

- **Be respectful** - Treat everyone with respect
- **Be constructive** - Provide constructive feedback
- **Be patient** - Be patient with newcomers
- **Be inclusive** - Welcome diverse perspectives

### Enforcement

Violations can be reported via [GitHub Issues](https://github.com/646826/claude-code-council/issues)

---

## 🙏 Thank You

Thank you for contributing to Claude Code Council! Your contributions help make code review better for everyone.

---

**Happy Contributing!** 🎉

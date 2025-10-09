# Installation Guide

Quick guide to install Claude Code Council plugin.

---

## Method 1: From GitHub (Recommended)

### Prerequisites

- Claude Code installed
- Git installed

### Steps

1. **Clone the repository**

```bash
git clone https://github.com/646826/claude-code-council.git
```

2. **Create a local marketplace**

```bash
# Create marketplace directory
mkdir -p ~/.claude-marketplaces/local

# Copy plugin to marketplace
cp -r claude-code-council ~/.claude-marketplaces/local/

# Create marketplace.json
mkdir -p ~/.claude-marketplaces/local/.claude-plugin
cat > ~/.claude-marketplaces/local/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "local-marketplace",
  "owner": {
    "name": "Local User",
    "email": "local@example.com"
  },
  "metadata": {
    "description": "Local Claude Code marketplace",
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

Start Claude Code in any project:

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
/plugin
```

You should see:

```
Installed plugins:
- claude-code-council@local-marketplace (v1.0.0)
```

---

## Method 2: Direct Installation

If you have the plugin directory already:

1. **Copy to plugins directory**

```bash
cp -r claude-code-council ~/.claude/plugins/
```

2. **Restart Claude Code**

The plugin should auto-load.

---

## Testing Installation

Run a test command:

```
/ai-council:council-config
```

You should see the plugin configuration.

---

## Troubleshooting

### Plugin not found

**Problem**: `Unknown plugin: claude-code-council`

**Solution**:

1. Check marketplace exists:
   ```bash
   ls ~/.claude-marketplaces/local/
   ```

2. Verify plugin directory:
   ```bash
   ls ~/.claude-marketplaces/local/claude-code-council/
   ```

3. Reinstall:
   ```
   /plugin uninstall claude-code-council@local-marketplace
   /plugin install claude-code-council@local-marketplace
   ```

### Commands not found

**Problem**: `Unknown slash command: council`

**Solution**: Use full namespace:

```
/ai-council:council-trivial test.ts
```

Or use Tab autocomplete:

```
/council<Tab>
```

### Permission errors

**Problem**: Permission denied when copying files

**Solution**: Use sudo (if necessary):

```bash
sudo cp -r claude-code-council ~/.claude-marketplaces/local/
```

---

## Updating

To update to a new version:

1. **Pull latest changes**

```bash
cd claude-code-council
git pull origin main
```

2. **Copy to marketplace**

```bash
cp -r . ~/.claude-marketplaces/local/claude-code-council/
```

3. **Reinstall in Claude Code**

```
/plugin uninstall claude-code-council@local-marketplace
/plugin install claude-code-council@local-marketplace
```

Restart Claude Code.

---

## Uninstalling

To remove the plugin:

1. **Uninstall from Claude Code**

```
/plugin uninstall claude-code-council@local-marketplace
```

2. **Remove marketplace (optional)**

```bash
rm -rf ~/.claude-marketplaces/local
```

---

## Next Steps

Once installed, see:

- **[README.md](./README.md)** - Full documentation
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - How to contribute
- **Commands** - Try `/council<Tab>` for autocomplete

---

**Happy reviewing!** 🎉

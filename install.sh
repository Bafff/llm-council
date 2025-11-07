#!/bin/bash
# LLM Council - Quick Install Script

set -e

echo "🤖 Installing LLM Council..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9+"
    exit 1
fi

# Install pipx
echo "📦 Checking pipx..."
if ! command -v pipx &> /dev/null; then
    echo "Installing pipx..."
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
fi

# Install LLM Council
echo "⚡ Installing LLM Council..."
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pipx install -e "$SCRIPT_DIR/llm_council"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Try: llm-council ask \"What is Docker?\""
echo "Or:  council models"
echo ""
echo "📖 Read: llm_council/QUICKSTART.md for more"

llm-council version

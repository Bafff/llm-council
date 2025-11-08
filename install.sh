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

if pipx list --short | grep -q "^llm-council"; then
    echo "🔁 LLM Council already installed via pipx – refreshing installation with --force"
    pipx install -e "$SCRIPT_DIR/llm_council" --force
else
    pipx install -e "$SCRIPT_DIR/llm_council"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Try: llm-council ask \"What is Docker?\""
echo "Or:  council models"
echo ""
echo "📖 Read: llm_council/QUICKSTART.md for more"

CANDIDATE_PATHS=""
if ! command -v llm-council &> /dev/null; then
    if command -v pipx &> /dev/null; then
        CANDIDATE_PATHS=$(PYTHONPATH="$SCRIPT_DIR" python3 - <<'PY'
from llm_council.utils.pipx_paths import discover_pipx_bin_paths

for path in discover_pipx_bin_paths():
    print(path)
PY
        )

        if [ -n "$CANDIDATE_PATHS" ]; then
            while IFS= read -r candidate; do
                if [ -n "$candidate" ] && [ -d "$candidate" ]; then
                    case ":$PATH:" in
                        *:"$candidate":*) ;;
                        *)
                            export PATH="$candidate:$PATH"
                            ;;
                    esac
                fi
            done <<EOF
$CANDIDATE_PATHS
EOF
        fi
    fi
fi

if command -v llm-council &> /dev/null; then
    if OUTPUT=$(llm-council version 2>&1); then
        echo "$OUTPUT"
    else
        echo "$OUTPUT"
        echo "⚠️  The 'llm-council' command is installed but failed to run."
        echo "   Please review the error above and report it if it persists."
    fi
else
    echo "⚠️  LLM Council is installed, but the 'llm-council' command is not yet on your PATH."
    if [ -n "$CANDIDATE_PATHS" ]; then
        echo "   Add one of the following directories to your PATH:"
        while IFS= read -r candidate; do
            if [ -n "$candidate" ]; then
                echo "     $candidate"
            fi
        done <<EOF
$CANDIDATE_PATHS
EOF
    else
        echo "   Run 'python3 -m pipx ensurepath' and restart your shell to update your PATH."
    fi
fi

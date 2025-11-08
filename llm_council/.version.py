"""Version information for LLM Council"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)

# Version history
VERSION_HISTORY = {
    "1.0.0": {
        "date": "2025-11-07",
        "changes": [
            "Initial release",
            "Multi-model consensus system",
            "Support for Claude, Gemini, GPT-4, Grok",
            "Weighted voting synthesis",
            "Beautiful CLI interface",
        ],
        "breaking_changes": [],
    }
}

# Next planned version
NEXT_VERSION = "1.1.0"
NEXT_VERSION_FEATURES = [
    "Web UI for non-technical users",
    "Browser cookie authentication",
    "History and analytics",
]


def get_version() -> str:
    """Get current version string"""
    return __version__


def get_version_info() -> dict:
    """Get detailed version information"""
    return {
        "version": __version__,
        "version_tuple": __version_info__,
        "latest_changes": VERSION_HISTORY.get(__version__, {}),
        "next_planned": {
            "version": NEXT_VERSION,
            "features": NEXT_VERSION_FEATURES,
        },
    }

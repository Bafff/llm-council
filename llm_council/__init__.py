"""
LLM Council - Multi-model AI consensus system

Get validated answers from multiple LLMs simultaneously.
"""

from pathlib import Path

__version__ = (Path(__file__).parent / "VERSION").read_text().strip()

__all__ = ["__version__"]

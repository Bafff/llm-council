#!/usr/bin/env python3
"""
LLM Council CLI - Consensus-based multi-model querying

Usage:
    python cli.py "What is the best way to learn Python?"
    python cli.py ask "Explain async/await in JavaScript"
    python cli.py models  # List available models
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, Sequence

import typer
from rich.console import Console
from rich.table import Table

from llm_council.core.council import LLMCouncil

app = typer.Typer(
    name="llm-council",
    help="🤖 LLM Council - Multi-model AI consensus system",
    add_completion=False
)

console = Console()


@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Your question for the council"),
    show_individual: bool = typer.Option(
        True,
        "--show-individual/--hide-individual",
        help="Show individual model responses"
    ),
    config: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to config.yaml"
    )
):
    """
    Ask a question to the LLM Council and get consensus answer.

    Examples:
        llm-council ask "What is quantum computing?"
        llm-council ask "Should I use TypeScript or JavaScript?" --show-individual
    """

    async def run():
        council = LLMCouncil(config_path=str(config) if config else None)

        # Temporarily override show_individual
        original = council.config.get('output', {}).get('show_individual_responses')
        if 'output' not in council.config:
            council.config['output'] = {}
        council.config['output']['show_individual_responses'] = show_individual

        result = await council.query(prompt)
        council.display_result(result)

        # Restore original
        if original is not None:
            council.config['output']['show_individual_responses'] = original

    asyncio.run(run())


@app.command()
def models(
    config: Path = typer.Option(
        None,
        "--config",
        "-c",
        help="Path to config.yaml"
    )
):
    """List all configured models and their status"""

    council = LLMCouncil(config_path=str(config) if config else None)

    table = Table(title="🤖 LLM Council Models")
    table.add_column("Model", style="cyan", no_wrap=True)
    table.add_column("Status", style="green")
    table.add_column("Weight", justify="right", style="yellow")
    table.add_column("Adapter", style="blue")

    for adapter in council.adapters:
        status = "✓ Available" if adapter.is_available() else "✗ Not available"
        status_style = "green" if adapter.is_available() else "red"

        table.add_row(
            adapter.model_name,
            f"[{status_style}]{status}[/{status_style}]",
            str(adapter.weight),
            adapter.__class__.__name__
        )

    console.print(table)

    # Show instructions for unavailable models
    unavailable = [a for a in council.adapters if not a.is_available()]
    if unavailable:
        console.print("\n[yellow]⚠️  Some models are unavailable. Check your API keys:[/yellow]")
        console.print("   - Gemini (FREE): https://ai.google.dev/")
        console.print("   - OpenRouter (cheap): https://openrouter.ai/")
        console.print("   - Claude: https://console.anthropic.com/")


@app.command()
def config(
    config_file: Path = typer.Option(
        None,
        "--file",
        "-f",
        help="Path to config.yaml to display"
    )
):
    """Show current configuration"""

    if not config_file:
        config_file = Path(__file__).parent / "config.yaml"

    if not config_file.exists():
        console.print(f"[red]✗ Config file not found: {config_file}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]📄 Configuration from {config_file}:[/cyan]\n")

    with open(config_file) as f:
        console.print(f.read())


@app.command()
def setup():
    """Interactive setup wizard for API keys"""

    console.print("[bold cyan]🚀 LLM Council Setup Wizard[/bold cyan]\n")

    env_file = Path(__file__).parent / ".env"

    if env_file.exists():
        overwrite = typer.confirm(
            ".env file already exists. Overwrite?",
            default=False
        )
        if not overwrite:
            console.print("[yellow]Setup cancelled.[/yellow]")
            return

    console.print("Let's set up your API keys. Press Enter to skip any.\n")

    # Gemini (FREE)
    console.print("[green]1. Gemini API Key (FREE! - Recommended)[/green]")
    console.print("   Get from: https://ai.google.dev/")
    gemini_key = typer.prompt("   Gemini API Key", default="", show_default=False)

    # Claude
    console.print("\n[cyan]2. Claude API Key (Optional)[/cyan]")
    console.print("   Get from: https://console.anthropic.com/")
    claude_key = typer.prompt("   Claude API Key", default="", show_default=False)

    # OpenRouter
    console.print("\n[blue]3. OpenRouter API Key (Optional - access to GPT-4, Grok)[/blue]")
    console.print("   Get from: https://openrouter.ai/")
    console.print("   $1 = 500+ queries!")
    openrouter_key = typer.prompt("   OpenRouter API Key", default="", show_default=False)

    # Write .env file
    with open(env_file, 'w') as f:
        f.write("# LLM Council API Keys\n\n")
        if gemini_key:
            f.write(f"GOOGLE_API_KEY={gemini_key}\n")
        if claude_key:
            f.write(f"ANTHROPIC_API_KEY={claude_key}\n")
        if openrouter_key:
            f.write(f"OPENROUTER_API_KEY={openrouter_key}\n")

    console.print(f"\n[green]✓ Configuration saved to {env_file}[/green]")
    console.print("\nTest it with:")
    console.print("  python cli.py ask \"What is 2+2?\"")


@app.command()
def version():
    """Show version information"""
    from pathlib import Path

    # Read version from VERSION file
    version_file = Path(__file__).parent / "VERSION"
    if version_file.exists():
        version_str = version_file.read_text().strip()
    else:
        version_str = "1.0.0"

    console.print(f"[cyan]LLM Council v{version_str}[/cyan]")
    console.print("Multi-model AI consensus system")
    console.print("\nBuilt on concepts from claude-code-council")
    console.print(f"\n[dim]See CHANGELOG.md for version history[/dim]")


# Default command (when no subcommand specified)


@app.callback(invoke_without_command=True)
def _root_command(ctx: typer.Context):
    """Show help when no command or prompt is provided."""

    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())


def _command_names() -> set[str]:
    """Return the registered command names, including Typer defaults."""

    names: set[str] = set()
    for command in app.registered_commands:
        raw_name = command.name or command.callback.__name__
        # Typer converts underscores to hyphens in CLI command names by default.
        names.add(raw_name.replace("_", "-"))
    return names


def main(argv: Optional[Sequence[str]] = None):
    """Entry point for pipx installation."""

    args = list(argv if argv is not None else sys.argv[1:])
    command_names = _command_names()

    if args and not args[0].startswith("-") and args[0] not in command_names:
        return app(args=["ask", *args])

    return app(args=args)


if __name__ == "__main__":
    main()

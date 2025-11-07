"""Main LLM Council Orchestrator - parallel multi-model querying"""

import asyncio
import yaml
from pathlib import Path
from typing import List, Dict, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from llm_council.adapters import ClaudeAdapter, GeminiAdapter, OpenRouterAdapter, BaseLLMAdapter
from llm_council.core.synthesizer import ConsensusSynthesizer, SynthesisResult


class LLMCouncil:
    """
    Main orchestrator for multi-model consensus system.

    Inspired by claude-code-council's parallel execution model.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.console = Console()

        # Load config
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"

        with open(config_path) as f:
            self.config = yaml.safe_load(f)

        # Initialize adapters
        self.adapters: List[BaseLLMAdapter] = []
        self._initialize_adapters()

        # Initialize synthesizer
        self.synthesizer = ConsensusSynthesizer(self.config)

    def _initialize_adapters(self):
        """Initialize all enabled model adapters"""

        adapter_map = {
            'claude': ClaudeAdapter,
            'gemini': GeminiAdapter,
            'openrouter': OpenRouterAdapter,
        }

        for model_name, model_config in self.config.get('models', {}).items():
            if not model_config.get('enabled', True):
                continue

            adapter_type = model_config.get('adapter')
            adapter_class = adapter_map.get(adapter_type)

            if not adapter_class:
                self.console.print(f"[yellow]⚠️  Unknown adapter type: {adapter_type}[/yellow]")
                continue

            try:
                adapter = adapter_class(model_config)
                self.adapters.append(adapter)
                self.console.print(
                    f"[green]✓[/green] Loaded {model_config['display_name']}"
                )
            except Exception as e:
                self.console.print(
                    f"[red]✗[/red] Failed to load {model_config['display_name']}: {e}"
                )

    async def query(self, prompt: str, **kwargs) -> SynthesisResult:
        """
        Query all models in parallel and synthesize results.

        Args:
            prompt: User's question
            **kwargs: Additional parameters for models

        Returns:
            SynthesisResult with consensus analysis
        """

        self.console.print(f"\n[bold cyan]🤖 LLM Council[/bold cyan]")
        self.console.print(f"[dim]Question:[/dim] {prompt}\n")

        # Check available adapters
        available_adapters = [a for a in self.adapters if a.is_available()]

        if not available_adapters:
            self.console.print("[red]❌ No models available! Check your API keys.[/red]")
            return self.synthesizer._error_result("No models available")

        self.console.print(
            f"[green]Querying {len(available_adapters)} models in parallel...[/green]\n"
        )

        # Execute queries in parallel with progress
        responses = await self._parallel_query(available_adapters, prompt, **kwargs)

        # Synthesize results
        self.console.print("\n[cyan]⚖️  Synthesizing consensus...[/cyan]\n")
        result = self.synthesizer.synthesize(responses, prompt)

        return result

    async def _parallel_query(
        self,
        adapters: List[BaseLLMAdapter],
        prompt: str,
        **kwargs
    ) -> List[Dict]:
        """
        Execute queries to all models in parallel.

        Inspired by claude-code-council:commands/council.md:39-47
        """

        results = []

        # Create progress display
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=self.console
        ) as progress:

            # Create tasks for each model
            tasks = []
            task_ids = []

            for adapter in adapters:
                task_id = progress.add_task(
                    f"[yellow]{adapter.model_name}",
                    total=100
                )
                task_ids.append(task_id)
                tasks.append(self._query_with_progress(adapter, prompt, progress, task_id, **kwargs))

            # Execute all in parallel
            responses = await asyncio.gather(*tasks, return_exceptions=True)

            # Collect results
            for adapter, response, task_id in zip(adapters, responses, task_ids):
                if isinstance(response, Exception):
                    self.console.print(f"[red]✗ {adapter.model_name}: {response}[/red]")
                    progress.update(task_id, completed=100, description=f"[red]✗ {adapter.model_name}")
                    continue

                if response.success:
                    results.append({
                        'adapter': adapter,
                        'response': response
                    })
                    progress.update(
                        task_id,
                        completed=100,
                        description=f"[green]✓ {adapter.model_name} ({response.latency_ms:.0f}ms)"
                    )
                else:
                    progress.update(
                        task_id,
                        completed=100,
                        description=f"[red]✗ {adapter.model_name}: {response.error}"
                    )

        return results

    async def _query_with_progress(
        self,
        adapter: BaseLLMAdapter,
        prompt: str,
        progress: Progress,
        task_id: int,
        **kwargs
    ):
        """Query a single adapter with progress updates"""

        # Start
        progress.update(task_id, completed=10)

        # Execute query
        response = await adapter.query(prompt, **kwargs)

        # Complete
        progress.update(task_id, completed=90)

        return response

    def display_result(self, result: SynthesisResult):
        """Display the synthesis result in a beautiful format"""

        from rich.panel import Panel
        from rich.markdown import Markdown

        # Consensus header
        consensus_emoji = {
            "strong": "✅",
            "moderate": "⚠️",
            "weak": "❓",
            "conflicted": "⚡"
        }

        emoji = consensus_emoji.get(result.consensus_level.value, "❓")
        confidence_pct = result.confidence_score * 100

        self.console.print(
            Panel(
                f"{emoji} **{result.consensus_level.value.upper()} CONSENSUS** "
                f"(Confidence: {confidence_pct:.1f}%)",
                style="bold"
            )
        )

        # Individual responses (if enabled)
        if self.config.get('output', {}).get('show_individual_responses', True):
            self.console.print("\n[bold]📋 Individual Responses:[/bold]\n")

            for resp in result.individual_responses:
                self.console.print(
                    Panel(
                        resp['content'][:500] + ("..." if len(resp['content']) > 500 else ""),
                        title=f"{resp['model']} (confidence: {resp['confidence']:.0%}, weight: {resp['weight']})",
                        border_style="blue"
                    )
                )

        # Synthesized answer
        self.console.print("\n[bold cyan]🎯 Synthesized Answer:[/bold cyan]\n")
        self.console.print(Markdown(result.synthesized_answer))

        # Meta-analysis
        if result.meta_analysis:
            self.console.print("\n[bold yellow]🔍 Meta-Analysis:[/bold yellow]\n")
            self.console.print(Markdown(result.meta_analysis))


async def main():
    """CLI entrypoint"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m core.council '<your question>'")
        sys.exit(1)

    prompt = " ".join(sys.argv[1:])

    council = LLMCouncil()
    result = await council.query(prompt)
    council.display_result(result)


if __name__ == "__main__":
    asyncio.run(main())

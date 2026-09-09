"""Rich terminal UI helpers for Aether CLI."""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "bold red",
        "success": "bold green",
        "user": "bold blue",
        "assistant": "bold magenta",
        "command": "bold yellow",
    }
)

console = Console(theme=custom_theme)


def print_banner(model: str) -> None:
    """Print the startup banner."""
    title = Text()
    title.append("✦ Aether CLI", style="bold magenta")
    title.append(" — Advanced AI Coding Assistant", style="dim")

    body = Text.from_markup(
        f"[dim]Model:[/dim] [cyan]{model}[/cyan]\n"
        f"[dim]Type your message or use[/dim] [command]/help[/command] [dim]for commands[/dim]"
    )

    console.print()
    console.print(Panel(body, title=title, border_style="magenta", padding=(1, 2)))
    console.print()


def print_user(message: str) -> None:
    """Print a user message."""
    console.print(Text("You › ", style="user"), end="")
    console.print(message)


def print_assistant_start() -> None:
    """Print the assistant prefix before streaming."""
    console.print(Text("Aether › ", style="assistant"), end="")


def print_markdown(text: str) -> None:
    """Render markdown content."""
    console.print(Markdown(text))


def print_info(message: str) -> None:
    console.print(f"[info]ℹ {message}[/info]")

def print_success(message: str) -> None:
    console.print(f"[success]✓ {message}[/success]")

def print_warning(message: str) -> None:
    console.print(f"[warning]⚠ {message}[/warning]")

def print_error(message: str) -> None:
    console.print(f"[error]✗ {message}[/error]")

def print_help() -> None:
    """Print available commands."""
    help_text = """
**Available Commands**

| Command | Description |
|---------|-------------|
| `/help` | Show this help message |
| `/clear` | Clear conversation history |
| `/model <name>` | Switch the current AI model |
| `/tools` | List available tools |
| `/exit` or `/q` | Exit Aether CLI |

**Tips**
- Just type normally to chat with the AI.
- Ask it to read files, write code, or run commands.
- Shell commands will ask for confirmation before running.
"""
    console.print(Panel(Markdown(help_text), title="Help", border_style="cyan"))

"""Main CLI entrypoint for Aether. Works on Windows, Linux, macOS and Termux."""

from __future__ import annotations

import platform
import sys

import typer
from rich.markdown import Markdown

from aether.chat import ChatEngine
from aether.config import get_settings
from aether.ui import (
    console,
    print_banner,
    print_error,
    print_help,
    print_info,
    print_success,
    print_warning,
)

app = typer.Typer(
    name="aether",
    help="Aether CLI — Advanced AI Coding Assistant",
    add_completion=False,
    rich_markup_mode="rich",
)


def run_interactive() -> None:
    """Start the interactive chat loop."""
    settings = get_settings()

    if not settings.has_any_key():
        print_error("No API key found.")
        console.print(
            "Please set at least one key in your [cyan].env[/cyan] file:\n"
            "  OPENAI_API_KEY, ANTHROPIC_API_KEY, XAI_API_KEY, GOOGLE_API_KEY, etc.\n"
            "See [cyan].env.example[/cyan] for details."
        )
        raise typer.Exit(code=1)

    engine = ChatEngine(settings)
    print_banner(engine.model)

    # Show platform tip for Termux users
    if "termux" in platform.platform().lower() or "com.termux" in str(sys.prefix):
        print_info("Running on Termux — all features are supported.")

    while True:
        try:
            user_input = console.input("[bold blue]You › [/bold blue]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print()
            print_info("Goodbye! Happy coding.")
            break

        if not user_input:
            continue

        # Handle slash commands
        if user_input.startswith("/"):
            cmd = user_input.lower().split()
            name = cmd[0]

            if name in ("/exit", "/q", "/quit"):
                print_info("Goodbye! Happy coding.")
                break

            elif name == "/help":
                print_help()
                continue

            elif name == "/clear":
                engine.clear_history()
                print_success("Conversation history cleared.")
                continue

            elif name == "/model":
                if len(cmd) < 2:
                    print_warning("Usage: /model <model-name>")
                    print_info(f"Current model: {engine.model}")
                    print_info("Examples: openai/gpt-4o | anthropic/claude-sonnet-4-20250514 | xai/grok-3")
                else:
                    new_model = " ".join(cmd[1:])
                    engine.set_model(new_model)
                    print_success(f"Switched to {new_model}")
                continue

            elif name == "/tools":
                from aether.tools import get_tools_schema

                tools = get_tools_schema()
                names = [t["function"]["name"] for t in tools]
                print_info("Available tools: " + ", ".join(names))
                continue

            elif name == "/info":
                from aether.tools import execute_tool
                info = execute_tool("get_system_info", {})
                console.print(info)
                continue

            else:
                print_warning(f"Unknown command: {name}. Type /help for help.")
                continue

        # Normal chat with tools
        console.print()
        with console.status("[bold magenta]Thinking...[/bold magenta]", spinner="dots"):
            response = engine.chat(user_input)

        if response:
            console.print("[bold magenta]Aether › [/bold magenta]")
            console.print(Markdown(response))
        console.print()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    model: str = typer.Option(
        None,
        "--model", "-m",
        help="Override the default model (e.g. openai/gpt-4o)",
    ),
) -> None:
    """Aether CLI — Advanced AI Coding Assistant."""
    if ctx.invoked_subcommand is not None:
        return

    settings = get_settings()
    if model:
        settings.model = model

    run_interactive()


if __name__ == "__main__":
    app()

"""Main CLI entrypoint for Aether. Works on Windows, Linux, macOS and Termux."""

from __future__ import annotations

import os
import platform
import sys
from datetime import datetime
from pathlib import Path

import typer
from rich.markdown import Markdown

from aether.chat import ChatEngine
from aether.config import get_settings, list_sessions, load_session, save_session
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
    help="Aether CLI — Advanced AI Coding Assistant by Sayanox",
    add_completion=False,
    rich_markup_mode="rich",
)


def _export_markdown(messages: list, path: str | None = None) -> str:
    if not path:
        path = f"aether-chat-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    lines = [
        "# Aether CLI Conversation\n",
        f"_Exported: {datetime.now().isoformat()}_\n",
        f"_Built by Sayanox_\n",
    ]
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content") or ""
        if role == "system":
            continue
        if role == "user":
            lines.append(f"## You\n\n{content}\n")
        elif role == "assistant":
            lines.append(f"## Aether\n\n{content}\n")
        elif role == "tool":
            name = msg.get("name", "tool")
            lines.append(f"### Tool `{name}`\n\n```\n{str(content)[:2000]}\n```\n")
    text = "\n".join(lines)
    Path(path).write_text(text, encoding="utf-8")
    return path


def run_interactive() -> None:
    settings = get_settings()

    if not settings.has_any_key():
        print_error("No API key found.")
        console.print(
            "Please set at least one key in your [cyan].env[/cyan] file:\n"
            "  OPENAI_API_KEY, ANTHROPIC_API_KEY, XAI_API_KEY, GOOGLE_API_KEY\n"
            "See [cyan].env.example[/cyan] for details."
        )
        raise typer.Exit(code=1)

    engine = ChatEngine(settings)
    print_banner(engine.model)

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

        if user_input.startswith("/"):
            cmd = user_input.split()
            name = cmd[0].lower()

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

                console.print(execute_tool("get_system_info", {}))
                continue
            elif name == "/pwd":
                print_info(os.getcwd())
                continue
            elif name == "/save":
                if len(cmd) < 2:
                    print_warning("Usage: /save <session-name>")
                else:
                    path = save_session(cmd[1], engine.messages)
                    print_success(f"Session saved to {path}")
                continue
            elif name == "/load":
                if len(cmd) < 2:
                    print_warning("Usage: /load <session-name>")
                    sessions = list_sessions()
                    if sessions:
                        print_info("Available sessions: " + ", ".join(sessions))
                    else:
                        print_info("No saved sessions found.")
                else:
                    data = load_session(cmd[1])
                    if data is None:
                        print_error(f"Session '{cmd[1]}' not found.")
                    else:
                        engine.messages = data
                        print_success(f"Loaded session '{cmd[1]}' ({len(data)} messages)")
                continue
            elif name == "/sessions":
                sessions = list_sessions()
                if sessions:
                    print_info("Saved sessions: " + ", ".join(sessions))
                else:
                    print_info("No saved sessions yet. Use /save <name>")
                continue
            elif name == "/export":
                out = cmd[1] if len(cmd) > 1 else None
                path = _export_markdown(engine.messages, out)
                print_success(f"Conversation exported to {path}")
                continue
            else:
                print_warning(f"Unknown command: {name}. Type /help for help.")
                continue

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
        "--model",
        "-m",
        help="Override the default model (e.g. openai/gpt-4o)",
    ),
) -> None:
    """Aether CLI — Advanced AI Coding Assistant by Sayanox."""
    if ctx.invoked_subcommand is not None:
        return

    settings = get_settings()
    if model:
        settings.model = model

    run_interactive()


if __name__ == "__main__":
    app()

"""Built-in tools for file system and shell operations."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from aether.ui import console, print_error, print_warning


def get_tools_schema() -> list[dict[str, Any]]:
    """Return OpenAI-compatible tool definitions."""
    return [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a file. Use this to examine source code or text files.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative or absolute path to the file",
                        }
                    },
                    "required": ["path"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write content to a file. Creates the file if it does not exist. Overwrites existing content.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Relative or absolute path to the file",
                        },
                        "content": {
                            "type": "string",
                            "description": "The full content to write to the file",
                        },
                    },
                    "required": ["path", "content"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_directory",
                "description": "List files and directories at the given path.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path (default: current working directory)",
                            "default": ".",
                        }
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "run_shell",
                "description": "Execute a shell command. Always ask the user for confirmation before running potentially destructive commands.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "The shell command to execute",
                        }
                    },
                    "required": ["command"],
                },
            },
        },
    ]


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    """Execute a tool by name and return the result as a string."""
    try:
        if name == "read_file":
            return _read_file(arguments.get("path", ""))
        elif name == "write_file":
            return _write_file(arguments.get("path", ""), arguments.get("content", ""))
        elif name == "list_directory":
            return _list_directory(arguments.get("path", "."))
        elif name == "run_shell":
            return _run_shell(arguments.get("command", ""))
        else:
            return f"Error: Unknown tool '{name}'"
    except Exception as e:
        return f"Error executing {name}: {e}"


def _read_file(path: str) -> str:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: File not found: {p}"
    if not p.is_file():
        return f"Error: Not a file: {p}"
    try:
        content = p.read_text(encoding="utf-8")
        # Limit very large files
        if len(content) > 100_000:
            content = content[:100_000] + "\n\n... [truncated for length]"
        return content
    except Exception as e:
        return f"Error reading file: {e}"


def _write_file(path: str, content: str) -> str:
    p = Path(path).expanduser().resolve()
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return f"Successfully wrote {len(content)} characters to {p}"
    except Exception as e:
        return f"Error writing file: {e}"


def _list_directory(path: str) -> str:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        return f"Error: Path not found: {p}"
    if not p.is_dir():
        return f"Error: Not a directory: {p}"

    entries = []
    try:
        for item in sorted(p.iterdir()):
            kind = "dir" if item.is_dir() else "file"
            size = item.stat().st_size if item.is_file() else "-"
            entries.append(f"{kind:4}  {size:>10}  {item.name}")
        if not entries:
            return "(empty directory)"
        return "\n".join(entries)
    except Exception as e:
        return f"Error listing directory: {e}"


def _run_shell(command: str) -> str:
    if not command.strip():
        return "Error: Empty command"

    # Safety: ask for confirmation on potentially dangerous commands
    dangerous_keywords = ["rm ", "rmdir", "del ", "format", "mkfs", "dd ", ">/dev/", "shutdown", "reboot"]
    is_dangerous = any(k in command.lower() for k in dangerous_keywords)

    console.print()
    print_warning(f"About to run shell command: {command}")
    if is_dangerous:
        print_warning("This command looks potentially destructive!")

    confirm = console.input("[bold yellow]Proceed? (y/N): [/bold yellow]").strip().lower()
    if confirm not in ("y", "yes"):
        return "Command cancelled by user."

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.getcwd(),
        )
        output = ""
        if result.stdout:
            output += result.stdout
        if result.stderr:
            output += ("\n" if output else "") + result.stderr
        if result.returncode != 0:
            output += f"\n[Exit code: {result.returncode}]"
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 60 seconds"
    except Exception as e:
        return f"Error running command: {e}"

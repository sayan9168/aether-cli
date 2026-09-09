"""Built-in tools for file system and shell operations. Cross-platform (Windows, Linux, Termux)."""

from __future__ import annotations

import os
import platform
import subprocess
from pathlib import Path
from typing import Any

from aether.ui import console, print_warning

IS_WINDOWS = platform.system() == "Windows"
IS_TERMUX = "com.termux" in os.environ.get("PREFIX", "") or "termux" in os.environ.get("HOME", "").lower()


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
                "description": "Write content to a file. Creates parent directories if needed. Overwrites existing content.",
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
                "name": "search_files",
                "description": "Search for a text pattern inside files (like grep). Useful to find code snippets.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Text or simple pattern to search for",
                        },
                        "path": {
                            "type": "string",
                            "description": "Directory or file to search in (default: current directory)",
                            "default": ".",
                        },
                    },
                    "required": ["pattern"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "run_shell",
                "description": "Execute a shell command. Always confirm with the user before running potentially destructive commands.",
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
        {
            "type": "function",
            "function": {
                "name": "get_system_info",
                "description": "Get basic system information (OS, Python version, current directory).",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
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
        elif name == "search_files":
            return _search_files(arguments.get("pattern", ""), arguments.get("path", "."))
        elif name == "run_shell":
            return _run_shell(arguments.get("command", ""))
        elif name == "get_system_info":
            return _get_system_info()
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
        content = p.read_text(encoding="utf-8", errors="replace")
        if len(content) > 120_000:
            content = content[:120_000] + "\n\n... [truncated for length]"
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
        for item in sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower())):
            kind = "dir " if item.is_dir() else "file"
            try:
                size = item.stat().st_size if item.is_file() else "-"
            except OSError:
                size = "?"
            entries.append(f"{kind}  {str(size):>10}  {item.name}")
        if not entries:
            return "(empty directory)"
        return "\n".join(entries)
    except Exception as e:
        return f"Error listing directory: {e}"


def _search_files(pattern: str, path: str) -> str:
    if not pattern:
        return "Error: Empty search pattern"
    root = Path(path).expanduser().resolve()
    if not root.exists():
        return f"Error: Path not found: {root}"

    results = []
    max_results = 40
    try:
        if root.is_file():
            files = [root]
        else:
            files = list(root.rglob("*"))

        for f in files:
            if not f.is_file():
                continue
            # Skip common binary / large dirs
            if any(part in f.parts for part in (".git", "node_modules", "__pycache__", ".venv", "venv")):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
                for i, line in enumerate(text.splitlines(), 1):
                    if pattern.lower() in line.lower():
                        results.append(f"{f}:{i}: {line.strip()[:200]}")
                        if len(results) >= max_results:
                            results.append("... (more results truncated)")
                            return "\n".join(results)
            except Exception:
                continue

        if not results:
            return f"No matches found for '{pattern}'"
        return "\n".join(results)
    except Exception as e:
        return f"Error searching: {e}"


def _run_shell(command: str) -> str:
    if not command.strip():
        return "Error: Empty command"

    dangerous = ["rm -rf", "rmdir /s", "del /f", "format", "mkfs", "dd if=", "shutdown", "reboot", ">/dev/"]
    is_dangerous = any(k in command.lower() for k in dangerous)

    console.print()
    print_warning(f"About to run: {command}")
    if is_dangerous:
        print_warning("This command looks potentially destructive!")

    try:
        confirm = console.input("[bold yellow]Proceed? (y/N): [/bold yellow]").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return "Command cancelled by user."

    if confirm not in ("y", "yes"):
        return "Command cancelled by user."

    try:
        # Use the appropriate shell
        if IS_WINDOWS:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=90,
                cwd=os.getcwd(),
            )
        else:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=90,
                cwd=os.getcwd(),
                executable="/bin/bash" if Path("/bin/bash").exists() else None,
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
        return "Error: Command timed out after 90 seconds"
    except Exception as e:
        return f"Error running command: {e}"


def _get_system_info() -> str:
    info = [
        f"OS: {platform.system()} {platform.release()}",
        f"Platform: {platform.platform()}",
        f"Python: {platform.python_version()}",
        f"Current directory: {os.getcwd()}",
        f"Is Termux: {IS_TERMUX}",
        f"Is Windows: {IS_WINDOWS}",
    ]
    return "\n".join(info)

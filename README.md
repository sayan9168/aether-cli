<div align="center">

# ✦ Aether CLI

**Advanced AI Coding Assistant for the Terminal**  
*Open-source Claude Code alternative — built by [Sayanox](https://sayanox-enterprises-private-limited.vercel.app/)*

[![GitHub stars](https://img.shields.io/github/stars/sayan9168/aether-cli?style=for-the-badge&logo=github)](https://github.com/sayan9168/aether-cli/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Termux-purple?style=for-the-badge)](#)

[Website](https://aether-cli-sayan9168s-projects.vercel.app) · [Docs](https://aether-cli-sayan9168s-projects.vercel.app/docs.html) · [Changelog](https://aether-cli-sayan9168s-projects.vercel.app/changelog.html) · [Report Bug](https://github.com/sayan9168/aether-cli/issues)

</div>

---

## Overview

**Aether CLI** is a production-ready, multi-provider AI coding agent that runs entirely in your terminal.  
It can read and write files, search your codebase, run shell commands (with safety confirmation), save sessions, and export conversations — inspired by Claude Code, fully open source.

| Feature | Status |
|--------|--------|
| Multi-provider (OpenAI, Claude, Grok, Gemini, DeepSeek…) | ✅ |
| File read / write / list | ✅ |
| Code search (grep-like) | ✅ |
| Safe shell execution | ✅ |
| Session save / load / export | ✅ |
| Windows + Termux support | ✅ |
| Beautiful Rich UI | ✅ |

---

## Quick Start

```bash
git clone https://github.com/sayan9168/aether-cli.git
cd aether-cli

python -m venv .venv

# Linux / macOS / Termux
source .venv/bin/activate

# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

pip install -e .
cp .env.example .env
```

Edit `.env` and add at least one API key:

```env
OPENAI_API_KEY=sk-...
# or ANTHROPIC_API_KEY=...
# or XAI_API_KEY=...

AETHER_MODEL=openai/gpt-4o
```

Run:

```bash
aether
# or
python -m aether
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/clear` | Clear conversation history |
| `/model <name>` | Switch model |
| `/tools` | List available tools |
| `/info` | System information |
| `/pwd` | Print working directory |
| `/save <name>` | Save session |
| `/load <name>` | Load session |
| `/sessions` | List saved sessions |
| `/export [file]` | Export chat to Markdown |
| `/exit` | Quit |

---

## Built-in Tools

The agent can call these tools automatically:

- `read_file` — read any text file
- `write_file` — create or overwrite files
- `list_directory` — list files & folders
- `search_files` — search text across the project
- `run_shell` — execute shell commands (asks confirmation)
- `get_system_info` — OS / Python / Termux detection

---

## Supported Models (examples)

```text
openai/gpt-4o
openai/gpt-4o-mini
anthropic/claude-sonnet-4-20250514
xai/grok-3
gemini/gemini-2.0-flash
```

Any [LiteLLM-supported provider](https://docs.litellm.ai/docs/providers) works.

---

## Termux (Android)

```bash
pkg install python git
git clone https://github.com/sayan9168/aether-cli.git
cd aether-cli
pip install -e .
cp .env.example .env
# edit .env
aether
```

---

## Project Structure

```text
aether-cli/
├── aether/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py          # Entry point & commands
│   ├── chat.py         # LLM + tool loop
│   ├── config.py       # Settings & sessions
│   ├── tools.py        # File / shell tools
│   └── ui.py           # Rich terminal UI
├── website/            # Landing page + docs
├── .env.example
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Safety

- Destructive shell commands require explicit `y` confirmation
- No automatic `rm -rf` or similar without your approval
- Keep API keys only in `.env` (never commit them)

---

## Contributing

Issues and PRs are welcome.  
If this project helps you, please **⭐ star the repo** — it really helps visibility.

---

## License

MIT License © 2026 **Sayan Mahata** ([Sayanox](https://sayanox-enterprises-private-limited.vercel.app/))

---

<div align="center">

**Built with ❤️ for developers who live in the terminal**

</div>

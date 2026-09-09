# Aether CLI by Sayanox

**Advanced AI Coding Assistant** — Open-source Claude Code alternative for the terminal.

[![GitHub stars](https://img.shields.io/github/stars/sayan9168/aether-cli?style=social)](https://github.com/sayan9168/aether-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Website:** [aether-cli-sayan9168s-projects.vercel.app](https://aether-cli-sayan9168s-projects.vercel.app)  
**Built by:** [Sayanox](https://sayanox-enterprises-private-limited.vercel.app/) — Sayan Mahata

Works on **Windows**, **Linux**, **macOS** and **Termux (Android)**.

Multi-provider • Interactive chat • File tools • Shell • Code search • Session save • Beautiful UI

---

## Topics (add these on GitHub for better discovery)

```
ai, cli, coding-assistant, claude-code, terminal, openai, anthropic, grok, xai, termux, python, llm, agent, developer-tools, sayanox
```

Go to the repo → ⚙️ (About section) → Topics → paste the above.

---

## Features

- **Multi-Provider AI**: OpenAI, Anthropic (Claude), xAI (Grok), Google Gemini, DeepSeek + any OpenAI-compatible API
- **Interactive Chat**: Natural conversation about your code
- **File Tools**: Read, write, list directories
- **Code Search**: Grep-like search across the project
- **Shell Execution**: Run commands with safety confirmation
- **Session Save/Load**: `/save`, `/load`, `/sessions`
- **Export Conversation**: `/export` to Markdown
- **System Info**: `/info`
- **Rich Terminal UI**: Colors, markdown, panels (works on Termux)
- **Cross-platform**: Windows, Linux, macOS, Termux

---

## Quick Install

```bash
git clone https://github.com/sayan9168/aether-cli.git
cd aether-cli
python -m venv .venv
source .venv/bin/activate          # Linux / macOS / Termux
# .venv\Scripts\activate           # Windows
pip install -e .
cp .env.example .env
# Add your API key in .env
aether
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/clear` | Clear conversation |
| `/model <name>` | Switch model |
| `/tools` | List tools |
| `/info` | System info |
| `/save <name>` | Save session |
| `/load <name>` | Load session |
| `/sessions` | List sessions |
| `/export [file]` | Export chat to Markdown |
| `/exit` | Quit |

---

## Supported Models (examples)

```
openai/gpt-4o
anthropic/claude-sonnet-4-20250514
xai/grok-3
gemini/gemini-2.0-flash
```

---

## License

MIT License © 2026 Sayan Mahata (Sayanox)

---

⭐ **Star this repo** if you find it useful — it helps more developers discover Aether CLI!

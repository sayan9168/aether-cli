# Aether CLI

**Advanced AI Coding Assistant** — A powerful terminal-based coding agent inspired by Claude Code.

Multi-provider support • Interactive chat • File system tools • Shell execution • Streaming responses • Beautiful terminal UI

---

## Features

- **Multi-Provider AI**: OpenAI, Anthropic (Claude), xAI (Grok), Google Gemini, DeepSeek, and any OpenAI-compatible API
- **Interactive Chat Mode**: Natural conversation with the AI about your code
- **File Tools**: Read, write, list, and search files in your project
- **Shell Execution**: Run terminal commands with confirmation (safe by default)
- **Streaming Responses**: Real-time token streaming for better UX
- **Rich Terminal UI**: Colors, markdown rendering, panels, and progress indicators
- **Session Commands**: `/help`, `/clear`, `/model`, `/tools`, `/exit`
- **Configurable**: Easy setup via `.env` file

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sayan9168/aether-cli.git
cd aether-cli
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# or
.venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -e .
# or
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# At least one is required
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=xai-...
GOOGLE_API_KEY=...

# Default model (examples below)
AETHER_MODEL=openai/gpt-4o
# AETHER_MODEL=anthropic/claude-sonnet-4-20250514
# AETHER_MODEL=xai/grok-3
# AETHER_MODEL=gemini/gemini-2.0-flash
```

---

## Usage

Start the interactive CLI:

```bash
aether
# or
python -m aether
```

### Example session

```
$ aether

✦ Aether CLI — Advanced AI Coding Assistant
Model: openai/gpt-4o

You > Explain the main function in main.py

Aether > [reads the file and explains...]

You > /model anthropic/claude-sonnet-4-20250514
Switched to anthropic/claude-sonnet-4-20250514

You > Refactor this function to be more efficient

Aether > [proposes code changes...]
```

### Available Commands

| Command          | Description                          |
|------------------|--------------------------------------|
| `/help`          | Show help message                    |
| `/clear`         | Clear conversation history           |
| `/model <name>`  | Switch AI model                      |
| `/tools`         | List available tools                 |
| `/exit` or `/q`  | Exit the CLI                         |

---

## Supported Models (via LiteLLM)

- `openai/gpt-4o`, `openai/gpt-4o-mini`, `openai/o1`, etc.
- `anthropic/claude-sonnet-4-20250514`, `anthropic/claude-opus-4-...`
- `xai/grok-3`, `xai/grok-2`
- `gemini/gemini-2.0-flash`, `gemini/gemini-1.5-pro`
- Any OpenAI-compatible endpoint

See [LiteLLM providers](https://docs.litellm.ai/docs/providers) for the full list.

---

## Project Structure

```
aether-cli/
├── aether/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py          # Main CLI entry + interactive loop
│   ├── config.py       # Configuration & environment
│   ├── chat.py         # Chat engine + streaming
│   ├── tools.py        # File & shell tools
│   └── ui.py           # Rich terminal UI helpers
├── .env.example
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Safety Notes

- Shell commands require explicit confirmation before execution.
- The tool only operates inside the current working directory by default.
- Never share your API keys. Keep `.env` out of version control.

---

## License

MIT License © 2026 Sayan Mahata

---

Built with ❤️ for developers who live in the terminal.

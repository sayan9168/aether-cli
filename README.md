# Aether CLI

**Advanced AI Coding Assistant** — A powerful terminal-based coding agent inspired by Claude Code.

Works seamlessly on **Windows**, **Linux**, **macOS** and **Termux (Android)**.

Multi-provider support • Interactive chat • File system tools • Shell execution • Code search • Streaming responses • Beautiful terminal UI

---

## Features

- **Multi-Provider AI**: OpenAI, Anthropic (Claude), xAI (Grok), Google Gemini, DeepSeek, and any OpenAI-compatible API
- **Interactive Chat Mode**: Natural conversation with the AI about your code
- **File Tools**: Read, write, list directories
- **Code Search**: Search text across your project (grep-like)
- **Shell Execution**: Run terminal commands with safety confirmation
- **System Info**: Detect OS, Termux, Python version etc.
- **Streaming + Tool Calling**: Full agentic loop
- **Rich Terminal UI**: Colors, markdown, panels (works on Termux too)
- **Session Commands**: `/help`, `/clear`, `/model`, `/tools`, `/info`, `/exit`
- **Cross-platform**: Tested design for Windows CMD/PowerShell and Termux

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

# Linux / macOS / Termux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install

```bash
pip install -e .
# or
pip install -r requirements.txt
```

### 4. Configure API keys

```bash
cp .env.example .env
```

Edit `.env` and add at least one key:

```env
OPENAI_API_KEY=sk-...
# or
ANTHROPIC_API_KEY=sk-ant-...
# or
XAI_API_KEY=xai-...

AETHER_MODEL=openai/gpt-4o
```

---

## Usage

```bash
aether
# or
python -m aether
```

### Example

```
$ aether

✦ Aether CLI — Advanced AI Coding Assistant
Model: openai/gpt-4o

You > Explain the main function in main.py
Aether > [reads the file and explains...]

You > /model xai/grok-3
Switched to xai/grok-3

You > Search for all TODO comments and list them
```

### Commands

| Command          | Description                     |
|------------------|---------------------------------|
| `/help`          | Show help                       |
| `/clear`         | Clear conversation history      |
| `/model <name>`  | Switch AI model                 |
| `/tools`         | List available tools            |
| `/info`          | Show system information         |
| `/exit` or `/q`  | Exit                            |

---

## Termux Notes

Aether works great on Termux:

```bash
pkg install python git
pip install -e .
```

Just make sure you have a good terminal (or Termux:Styling) for the best colors.

---

## Windows Notes

Works out of the box on Windows 10/11 with PowerShell or CMD.  
Use `python -m aether` if the `aether` command is not found in PATH.

---

## License

MIT License © 2026 Sayan Mahata

---

Built with ❤️ for developers who live in the terminal.

# AI Coding Agent

A terminal-based AI coding agent built in Python, powered by Google Gemini. The agent can inspect, run, and modify files within a sandboxed working directory — including autonomously diagnosing and fixing bugs.

---

## Features

- Lists files and directories within the working directory
- Reads file contents (up to a configurable character limit)
- Executes Python files with optional arguments
- Writes and overwrites files
- Iterative tool-calling loop — the agent plans and executes multi-step tasks autonomously
- Sandboxed: all file operations are restricted to the configured working directory

---

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (package manager)
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)

---

## Setup

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd <repo-directory>
   ```

2. Install dependencies:
    ```bash
    uv sync
    ```

3. Create a .env file in the project root with your Gemini API key:
    ```bash
    GEMINI_API_KEY=your_api_key_here
    ```

---

## Usage

- Run the agent with a natural-language prompt:
   ```bash
   uv run main.py "Your prompt here"
   ```


- Enable verbose output to see token counts and function call results:
    ```bash
    uv run main.py "Your prompt here" --verbose
    ```

- Example:
    ```bash
    uv run main.py "how does the calculator render results to the console?" --verbose
    ```

## Configuration

Edit `config.py` to adjust behaviour:

| Variable      | Default        | Description                                      |
|---------------|----------------|--------------------------------------------------|
| `WORKING_DIR` | `./calculator` | The directory the agent is allowed to operate in |
| `MAX_CHARS`   | `10000`        | Maximum characters read from any single file     |
| `MAX_ITERS`   | `20`           | Maximum agentic loop iterations per run          |

---

**Warning:** This is a learning project built for educational purposes only. It is not intended for production use. Use at your own risk.

Built as part of the [Boot.dev](https://www.boot.dev) "Build an AI Agent in Python" course.

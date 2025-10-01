# Terminal Coding Assistant

A terminal-based AI coding assistant (HF Token) via HuggingFace.

## Features

- 📁 **File Operations**: Read, write, and edit files with intelligent context awareness
- 🔍 **Code Search**: Search files using glob patterns and grep for code patterns
- 🛠️ **Shell Integration**: Execute bash/shell commands (git, npm, pip, etc.)
- 💬 **Interactive Chat**: Natural conversation with streaming responses
- 🤖 **Tool Calling**: AI can autonomously use tools to complete tasks

## Installation

> **Quick Start:** See [install/QUICKSTART.md](install/QUICKSTART.md) for a simple 4-step guide.

### Quick Setup (4 Steps)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install package:**
   ```bash
   pip install -e .
   ```

3. **Add to PATH (Windows):**
   ```bash
   install\setup_path.bat
   ```

   For Linux/Mac, see [install/INSTALL.md](install/INSTALL.md)

4. **Restart terminal and run:**
   ```bash
   termicode
   ```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd termicode
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install as global command:
   ```bash
   pip install -e .
   ```

4. Add Python Scripts to PATH - see [install/INSTALL.md](install/INSTALL.md) for detailed instructions.

5. Restart terminal and test:
   ```bash
   termicode
   ```

### Configuration

Configure `.env` file:
```bash
# Required: HuggingFace API Token
HF_TOKEN='your-huggingface-token'

# Optional: AI Model (default: deepseek-ai/DeepSeek-V3.2-Exp)
MODEL=deepseek-ai/DeepSeek-V3.2-Exp

# Optional: Display Mode (default: SILENT)
MODE=SILENT  # Hide JSON tool calls
# MODE=DEBUG  # Show JSON tool calls for debugging
```

Get your HuggingFace token from: https://huggingface.co/settings/tokens

## Usage

### Method 1: Global Command (Recommended)

If you installed with `pip install -e .`, simply run:
```bash
termicode
```

This works from any directory and will use that directory as the working context!

### Method 2: Direct Python

Run from the project directory:
```bash
python main.py
```

### Method 3: Using Script Launcher

**Windows:**
```bash
termicode.bat
```

**Linux/Mac:**
```bash
chmod +x termicode.sh
./termicode.sh
```

### UI Demo

Try the UI demo to see all features:
```bash
python demo_ui.py
```

### Available Commands

- Type your questions or requests naturally
- `clear` - Clear conversation history
- `pwd` - Show current working directory
- `exit` or `quit` - Exit the assistant

### Features

🎨 **Interactive UI:**
- Animated loading spinners while AI thinks
- Clean diff viewer for code changes
- Color-coded file operations
- Progress indicators
- Only shows meaningful changes (not verbose logs)

### Example Interactions

```
You ▶ Show me all Python files in this project
You ▶ Read the contents of src/assistant.py
You ▶ Add error handling to the main function
You ▶ Run the tests using pytest
You ▶ Search for all TODO comments in the codebase
```

## Available Tools

The AI assistant has access to these tools:

1. **read_file** - Read file contents with line numbers
2. **write_file** - Create new files or overwrite existing ones
3. **edit_file** - Edit files by replacing specific text
4. **glob** - Find files matching patterns (e.g., `**/*.py`)
5. **grep** - Search for regex patterns in files
6. **bash** - Execute shell commands

## Project Structure

```
termicode/
├── main.py                      # CLI entry point
├── setup.py                     # Package setup configuration
├── requirements.txt             # Python dependencies
├── README.md                    # Main documentation
├── .env                         # Configuration (HF_TOKEN, MODEL, MODE)
│
├── install/                     # Installation files
│   ├── setup_path.bat          # Auto PATH setup (Windows)
│   ├── add_to_path.ps1         # PowerShell PATH script
│   ├── termicode.bat           # Windows launcher
│   ├── termicode.sh            # Linux/Mac launcher
│   ├── QUICKSTART.md           # Quick start guide
│   ├── INSTALL.md              # Detailed installation
│   └── README.md               # Install folder docs
│
├── src/                         # Source code
│   ├── ai_client.py            # HuggingFace API wrapper
│   ├── assistant.py            # Main assistant logic
│   ├── prompts.py              # System prompts
│   ├── tools/                  # Tool implementations
│   │   ├── base.py             # Base tool classes
│   │   ├── file_tools.py       # File operation tools
│   │   └── bash_tool.py        # Shell command tool
│   └── utils/                  # Utility modules
│       ├── tool_executor.py    # Tool execution engine
│       ├── response_parser.py  # Parse AI responses
│       ├── interactive_executor.py  # Interactive UI executor
│       ├── diff_viewer.py      # Code diff display
│       └── ui_helpers.py       # Terminal UI components
│
└── tests/                       # Test files
    └── demo_ui.py              # UI demo
```

## How It Works

1. **User Input**: You type a natural language request
2. **AI Processing**: DeepSeek-V3.2 analyzes your request and decides which tools to use
3. **Tool Execution**: The assistant executes the necessary tools (read files, run commands, etc.)
4. **Response**: You receive a comprehensive answer with the results

## Configuration

All configuration is done via the `.env` file:

### AI Model

Change the AI model by setting `MODEL` in `.env`:
```bash
MODEL=deepseek-ai/DeepSeek-V3.2-Exp
# Or use other HuggingFace models like:
# MODEL=meta-llama/Llama-3.1-70B-Instruct
# MODEL=Qwen/Qwen2.5-72B-Instruct
```

### Display Mode

Set `MODE` in `.env` file:
- **SILENT** (default): Hides JSON tool calls for clean output
- **DEBUG**: Shows JSON tool calls for debugging

```bash
MODE=SILENT  # Clean output
MODE=DEBUG   # Show all tool calls
```

### Customize System Prompt

Edit `src/prompts.py` to modify the `SYSTEM_PROMPT` variable.

## Requirements

- Python 3.8+
- HuggingFace account and API token
- openai Python package (for API compatibility)

## Troubleshooting

**Error: HF_TOKEN not set**
- Make sure you've exported your HuggingFace token: `export HF_TOKEN='your-token'`

**Import errors**
- Ensure you're running from the project root directory
- Check that all dependencies are installed: `pip install -r requirements.txt`

**Command not working**
- The assistant uses shell commands, make sure the required tools are installed on your system

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

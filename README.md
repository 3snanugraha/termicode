# Terminal Coding Assistant

A terminal-based AI coding assistant (HF Token) via HuggingFace.

## Features

- 📁 **File Operations**: Read, write, and edit files with intelligent context awareness
- 🔍 **Code Search**: Search files using glob patterns and grep for code patterns
- 🛠️ **Shell Integration**: Execute bash/shell commands (git, npm, pip, etc.)
- 💬 **Interactive Chat**: Natural conversation with streaming responses
- 🤖 **Tool Calling**: AI can autonomously use tools to complete tasks

## Installation

### Prerequisites

Before installing, make sure you have:
- **Python 3.8 or higher** installed
- **pip** package manager
- **HuggingFace account** (free) - Sign up at https://huggingface.co/join
- **Git** (optional, for cloning)

### Step-by-Step Installation Guide

#### Step 1: Get the Code

**Option A: Clone with Git (recommended)**
```bash
git clone https://github.com/yourusername/termicode.git
cd termicode
```

**Option B: Download ZIP**
- Download and extract the ZIP file
- Open terminal/command prompt in the extracted folder

#### Step 2: Install Python Dependencies

Install required packages:
```bash
pip install -r requirements.txt
```

This installs:
- `openai>=1.0.0` - For API compatibility with HuggingFace
- `python-dotenv>=1.0.0` - For environment variable management

#### Step 3: Install Termicode as Global Command

Install the package in editable mode:
```bash
pip install -e .
```

**What this does:**
- Creates a global `termicode` command
- Links to your local code (changes take effect immediately)
- No need to reinstall after code updates

#### Step 4: Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

**Windows:**
```bash
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

Edit the `.env` file and add your HuggingFace token:
```bash
# Required: HuggingFace API Token
HF_TOKEN=hf_your_actual_token_here

# Optional: AI Model (default shown below)
MODEL=deepseek-ai/DeepSeek-V3.2-Exp

# Optional: Display Mode (SILENT or DEBUG)
MODE=SILENT
```

**How to get HuggingFace Token:**
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Give it a name (e.g., "termicode")
4. Select "Read" permission (sufficient for API calls)
5. Copy the token (starts with `hf_`)
6. Paste it in your `.env` file

#### Step 5: Verify Installation

Test if termicode is working:
```bash
termicode
```

If successful, you should see:
```
✓ AI assistant ready!

╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        Terminal Coding Assistant                           ║
║                                                            ║
║  AI-powered coding assistant for your terminal             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

You ▶
```

Type `exit` to quit.

### Troubleshooting Common Issues

#### Issue 1: "ModuleNotFoundError: No module named 'main'"

**Solution:** Reinstall the package correctly:
```bash
pip uninstall termicode
pip install -e .
```

#### Issue 2: "termicode: command not found" (Windows)

**Problem:** Python Scripts folder is not in PATH.

**Solution:** Add Python Scripts to PATH automatically:
```bash
install\setup_path.bat
```

Then **restart your terminal** and try again.

**Manual solution (if script doesn't work):**
1. Find your Python installation path (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\`)
2. Add `Scripts` subfolder to PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" variable
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python3XX\Scripts`
3. Restart terminal

#### Issue 3: "termicode: command not found" (Linux/Mac)

**Solution:** Make sure pip installs to a directory in your PATH:
```bash
# Check where pip installs scripts
python3 -m site --user-base

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

#### Issue 4: "HF_TOKEN environment variable is not set!"

**Solution:** Make sure your `.env` file exists and contains your token:
```bash
# Check if .env exists
ls -la .env  # Linux/Mac
dir .env     # Windows

# Verify .env content (should show HF_TOKEN=hf_...)
cat .env  # Linux/Mac
type .env # Windows
```

#### Issue 5: "EOF when reading a line" (infinite loop)

**Solution:** This is fixed in the latest version. Make sure you have the updated `main.py` with EOFError handling.

### Advanced Configuration

#### Changing AI Model

You can use any HuggingFace model that supports chat completion:
```bash
# In .env file
MODEL=meta-llama/Llama-3.1-70B-Instruct
# or
MODEL=Qwen/Qwen2.5-72B-Instruct
```

#### Debug Mode

To see JSON tool calls (useful for debugging):
```bash
# In .env file
MODE=DEBUG
```

#### Custom System Prompt

Edit `src/prompts.py` to customize the AI's behavior.

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

## Requirements

- Python 3.8+
- HuggingFace account and API token
- openai Python package (for API compatibility)
- python-dotenv for environment variable management

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

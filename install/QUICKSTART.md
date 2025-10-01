# Quick Start Guide

## 🚀 Installation (4 Steps)

```bash
# Step 1: Install dependencies (from termicode root directory)
pip install -r requirements.txt

# Step 2: Install package
pip install -e .

# Step 3: Add to PATH
install\setup_path.bat

# Step 4: Close terminal, open new one, then run:
termicode
```

## ✅ What You Just Did

✓ Installed `termicode` package globally
✓ Added Python Scripts to your PATH
✓ Can now run `termicode` from ANY folder!

## 🎯 How to Use

### Start the Assistant
```bash
cd your-project-folder
termicode
```

The assistant will use `your-project-folder` as the working directory!

### Example Commands

**Read files:**
```
You ▶ Read the README.md file
You ▶ Show me all Python files
```

**Write/Edit code:**
```
You ▶ Create a new file called hello.py with a hello world function
You ▶ Add error handling to main.py
```

**Search:**
```
You ▶ Search for all TODO comments
You ▶ Find all files containing "import requests"
```

**Run commands:**
```
You ▶ Run the tests
You ▶ Install the requirements
You ▶ Check git status
```

## 🛠️ Configuration

Edit `.env` file in the termicode directory:

```bash
# Required
HF_TOKEN=your-huggingface-token

# Optional (defaults shown)
MODEL=deepseek-ai/DeepSeek-V3.2-Exp
MODE=SILENT
```

### Display Modes

- `MODE=SILENT` - Clean output (recommended)
- `MODE=DEBUG` - Show JSON tool calls (for debugging)

## 🔧 Troubleshooting

**"termicode is not recognized"**
1. Make sure you ran `install\setup_path.bat` from the termicode root directory
2. Close and reopen your terminal
3. Check PATH includes: `C:\Users\user\AppData\Local\Programs\Python\Python313\Scripts`

**"HF_TOKEN not set"**
1. Go to: https://huggingface.co/settings/tokens
2. Create a token
3. Add to `.env` file in termicode folder: `HF_TOKEN=your-token`

**Still having issues?**
See [INSTALL.md](INSTALL.md) for detailed instructions.

## 📚 More Info

- Full documentation: [README.md](../README.md)
- Installation details: [INSTALL.md](INSTALL.md)

---

**Created by Tris**

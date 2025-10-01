# Installation Files

This folder contains all installation and setup scripts for Termicode.

## Files

### Setup Scripts

- **`setup_path.bat`** - Windows batch script to automatically add Python Scripts to PATH
- **`add_to_path.ps1`** - PowerShell script for PATH setup (alternative method)

### Launcher Scripts

- **`termicode.bat`** - Windows launcher script
- **`termicode.sh`** - Linux/Mac launcher script

### Documentation

- **`QUICKSTART.md`** - Quick start guide (4-step installation)
- **`INSTALL.md`** - Detailed installation instructions

## Quick Install

From the termicode root directory:

```bash
# Step 1: Install dependencies
pip install -r requirements.txt

# Step 2: Install package
pip install -e .

# Step 3: Add to PATH (Windows)
install\setup_path.bat

# Step 4: Restart terminal and run
termicode
```

For full documentation, see [QUICKSTART.md](QUICKSTART.md) or [INSTALL.md](INSTALL.md).

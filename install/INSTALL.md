# Installation Guide

## Quick Install (Windows)

### Step 1: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install the package
```bash
pip install -e .
```

### Step 3: Add to PATH (Choose one method)

**Method A: Automatic (Recommended)**
Double-click: `setup_path.bat`

Or run in terminal:
```bash
setup_path.bat
```

**Method B: PowerShell Script**
```bash
powershell -ExecutionPolicy Bypass -File add_to_path.ps1
```

**Method C: Manual**
1. Press `Win + R` → type `sysdm.cpl` → Enter
2. Go to "Advanced" tab → "Environment Variables"
3. Under "User variables", select "Path" → "Edit"
4. Click "New" and add: `C:\Users\user\AppData\Local\Programs\Python\Python313\Scripts`
5. Click OK on all dialogs

### Step 4: Restart Terminal
**IMPORTANT:** Close and reopen your terminal/command prompt for PATH changes to take effect.

### Step 5: Test Installation
```bash
termicode
```

You should see the Terminal Coding Assistant start up!

## Alternative Methods

### Method 1: Using Batch File (Windows)

1. Copy `termicode.bat` to a folder in your PATH (e.g., `C:\Windows`)
2. Run from anywhere: `termicode`

### Method 2: Add Project to PATH

Add the project directory to your PATH, then run `termicode.bat` directly.

### Method 3: Create Alias (PowerShell)

Add to your PowerShell profile (`$PROFILE`):
```powershell
function termicode { python "C:\Users\user\Project\termicode\main.py" }
```

## Linux/Mac Setup

1. **Install:**
   ```bash
   pip install -e .
   ```

2. **Make script executable:**
   ```bash
   chmod +x termicode.sh
   ```

3. **Create symlink (optional):**
   ```bash
   sudo ln -s $(pwd)/termicode.sh /usr/local/bin/termicode
   ```

4. **Run from anywhere:**
   ```bash
   termicode
   ```

## Troubleshooting

**"termicode is not recognized"**
- Make sure Python Scripts directory is in PATH
- Restart your terminal after adding to PATH
- Try using full path: `C:\Users\...\Scripts\termicode.exe`

**"No module named 'src'"**
- Make sure you're running from the project directory
- Or use the installed package (after `pip install -e .`)

**"HF_TOKEN not set"**
- Create `.env` file in the project directory
- Add your HuggingFace token: `HF_TOKEN=your-token-here`

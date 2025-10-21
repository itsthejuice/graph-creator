# How to Run Graph Creator

## Super Simple Instructions 🚀

```bash
cd /home/admin/Projects/graph-creator
./run.sh
```

**That's literally it!** 🎉

---

## What Will Happen

### First Time Running

```
1. Script checks you have Python 3.11+  ✓
2. Creates virtual environment          ✓
3. Installs all dependencies            ✓ (takes 2-3 minutes)
4. Launches the application             ✓
```

### Every Time After

```
1. Script checks setup is complete      ✓
2. Launches the application             ✓ (takes 2 seconds!)
```

---

## Troubleshooting

### Problem: "pip install -e ." fails with setuptools error

**Solution:** Already fixed! Just run:
```bash
./run.sh
```

The new `run.sh` script handles everything automatically.

### Problem: Need to start fresh

**Solution:**
```bash
./run.sh --clean
./run.sh
```

### Problem: Dependencies seem broken

**Solution:**
```bash
./run.sh --reinstall
```

---

## What Got Fixed

1. ✅ **Fixed setuptools error** - Added explicit package configuration
2. ✅ **Automated venv creation** - No more manual setup
3. ✅ **Smart dependency installation** - Only installs once
4. ✅ **Fast subsequent launches** - Skips setup when done
5. ✅ **Better error messages** - Know what went wrong
6. ✅ **Easy recovery** - `--clean` and `--reinstall` options

---

## File Changes Made

### `pyproject.toml`
- Added `[tool.setuptools.packages.find]` section
- Explicitly includes `app*` packages
- Excludes `tests*` and `assets*`

### `run.sh`
- Complete rewrite with smart setup detection
- Auto-creates and activates virtual environment
- Only installs dependencies when needed
- Colorful, user-friendly output
- Command options: `--clean`, `--reinstall`, `--help`

### `.gitignore`
- Added `.setup_complete` marker file
- venv already excluded

### Documentation
- Updated `README.md` with new instructions
- Updated `INSTALLATION.md` with script details
- Created `QUICKSTART.md` for quick reference
- Created `SETUP_FIXES.md` for technical details

---

## Example Run (First Time)

```bash
$ ./run.sh
========================================
   Graph Creator - Startup Script
========================================

[1/5] Checking Python version...
✓ Python 3.12 detected

[2/5] Checking virtual environment...
Creating virtual environment...
✓ Virtual environment created

[3/5] Activating virtual environment...
✓ Virtual environment activated

[4/5] Checking dependencies...
Installing dependencies (this may take a few minutes)...
[... pip install output ...]
✓ Dependencies installed successfully

[5/5] Starting Graph Creator...

========================================
Application is starting...
Press Ctrl+C to exit
========================================

[Flet window opens with Graph Creator UI]
```

---

## Example Run (Subsequent Times)

```bash
$ ./run.sh
========================================
   Graph Creator - Startup Script
========================================

[1/5] Checking Python version...
✓ Python 3.12 detected

[2/5] Checking virtual environment...
✓ Virtual environment already exists

[3/5] Activating virtual environment...
✓ Virtual environment activated

[4/5] Checking dependencies...
✓ Dependencies already installed

[5/5] Starting Graph Creator...

========================================
Application is starting...
Press Ctrl+C to exit
========================================

[Application launches immediately - ~2 seconds total!]
```

---

## All Available Commands

```bash
# Normal run (recommended)
./run.sh

# Remove everything and start fresh
./run.sh --clean

# Force reinstall dependencies (keeps venv)
./run.sh --reinstall

# Show help message
./run.sh --help
```

---

## System Requirements

- ✅ Python 3.11 or higher (you have 3.12 ✓)
- ✅ pip (comes with Python)
- ✅ ~500 MB disk space
- ✅ Display server for GUI (desktop Linux or WSL2 with X)

---

## Quick Test

Want to make sure everything works? Run:

```bash
cd /home/admin/Projects/graph-creator
./run.sh --clean  # Start fresh
./run.sh          # Should install and launch
```

If the GUI window opens with a chart, **you're all set!** 🎉

---

## Getting Help

1. **Quick reference:** `QUICKSTART.md`
2. **Installation help:** `INSTALLATION.md`
3. **User guide:** `USAGE.md`
4. **Technical details:** `SETUP_FIXES.md`
5. **Script help:** `./run.sh --help`

---

## Summary

**Before the fix:**
- Had to manually create venv
- Had to manually pip install
- Setuptools errors
- Complex setup process

**After the fix:**
- Just run `./run.sh`
- Everything automated
- No errors
- 2-second launch after first setup

**Bottom line:** Just run `./run.sh` and you're good to go! 🚀

---

**Ready to create beautiful charts!** 📊✨


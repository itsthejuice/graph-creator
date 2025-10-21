# Quick Start Guide

## TL;DR - Get Started in 10 Seconds

```bash
cd /home/admin/Projects/graph-creator
./run.sh
```

**Done!** The application will open automatically.

---

## What the Script Does

The `run.sh` script is your all-in-one launcher that:

### First Run
1. ✅ Checks Python 3.11+ is installed
2. ✅ Creates virtual environment (`venv/`)
3. ✅ Installs all dependencies (~2-3 minutes)
4. ✅ Launches Graph Creator

### Subsequent Runs
1. ✅ Checks Python version
2. ✅ Uses existing virtual environment
3. ✅ Skips dependency installation (already done!)
4. ✅ Launches Graph Creator immediately

**Time to launch after first setup: ~2 seconds**

---

## Script Commands

```bash
# Run the application (normal usage)
./run.sh

# Clean everything and start fresh
./run.sh --clean

# Force reinstall dependencies
./run.sh --reinstall

# Show help
./run.sh --help
```

---

## First Time Setup Example

```
$ ./run.sh
========================================
   Graph Creator - Startup Script
========================================

[1/5] Checking Python version...
✓ Python 3.11 detected

[2/5] Checking virtual environment...
Creating virtual environment...
✓ Virtual environment created

[3/5] Activating virtual environment...
✓ Virtual environment activated

[4/5] Checking dependencies...
Installing dependencies (this may take a few minutes)...
✓ Dependencies installed successfully

[5/5] Starting Graph Creator...

========================================
Application is starting...
Press Ctrl+C to exit
========================================
```

---

## Second Run Example (Fast!)

```
$ ./run.sh
========================================
   Graph Creator - Startup Script
========================================

[1/5] Checking Python version...
✓ Python 3.11 detected

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
```

---

## Common Use Cases

### Just Run the App
```bash
./run.sh
```

### Start Fresh (Remove All Setup)
```bash
./run.sh --clean
./run.sh  # Fresh install
```

### Something Broken? Reinstall Dependencies
```bash
./run.sh --reinstall
```

### Stop the Application
Press `Ctrl+C` in the terminal

---

## Troubleshooting

### "Permission denied"
```bash
chmod +x run.sh
./run.sh
```

### "Python 3.11 required"
Install Python 3.11 or higher:
```bash
# Debian/Ubuntu
sudo apt update
sudo apt install python3.11

# Or use your system's package manager
```

### "Virtual environment activation failed"
Try manual setup:
```bash
./run.sh --clean
python3 -m venv venv
source venv/bin/activate
pip install -e .
python -m app.main
```

### Dependencies Installation Failed
Check internet connection and try:
```bash
./run.sh --reinstall
```

---

## File Structure

After first run, you'll see:

```
graph-creator/
├── venv/              # Virtual environment (auto-created)
├── .setup_complete    # Marker file (auto-created)
├── app/               # Application code
├── tests/             # Test suite
├── run.sh             # This script!
└── ...
```

**Note:** `venv/` and `.setup_complete` are git-ignored.

---

## Manual Alternative

If you prefer manual control:

```bash
# One-time setup
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Every time you want to run
source venv/bin/activate
python -m app.main
```

But honestly, just use `./run.sh` — it's easier! 😊

---

## What Happens on Launch

When the app starts:
1. 📊 Window opens with two panes
2. 📈 Example "Overlapping Trends" chart loads automatically
3. 🎨 You can immediately start customizing
4. 💾 Use keyboard shortcuts (Ctrl+S to save, Ctrl+E to export)

---

## Need Help?

- **Full User Guide**: See `USAGE.md`
- **Installation Help**: See `INSTALLATION.md`
- **Project Details**: See `PROJECT_SUMMARY.md`
- **Script Help**: Run `./run.sh --help`

---

**Happy charting!** 📊✨


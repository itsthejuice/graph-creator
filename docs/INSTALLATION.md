# Installation and Quick Start Guide

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- 500 MB free disk space

## Step-by-Step Installation

### Quick Start (Recommended)

The **easiest and recommended** way to install and run Graph Creator:

```bash
cd /home/admin/Projects/graph-creator
./run.sh
```

**That's it!** The script automatically:
1. ✅ Checks Python 3.11+ is installed
2. ✅ Creates virtual environment (venv/)
3. ✅ Installs all dependencies
4. ✅ Launches the application
5. ✅ Skips setup on subsequent runs

### Manual Installation

If you prefer manual control:

#### 1. Navigate to Project Directory

```bash
cd /home/admin/Projects/graph-creator
```

#### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies

**Option A: Standard Installation (Recommended)**

```bash
pip install -e .
```

This installs:
- flet (UI framework)
- matplotlib (chart rendering)
- pandas (data manipulation)
- numpy (numerical operations)
- pydantic (data validation)
- scipy (scientific computing)
- openpyxl (Excel support)

**Option B: With Interactive Features**

```bash
pip install -e ".[interactive]"
```

Adds:
- plotly (interactive charts)
- kaleido (Plotly export)

**Option C: With Development Tools**

```bash
pip install -e ".[dev]"
```

Adds:
- pytest (testing)
- pytest-cov (coverage)

**Option D: Everything**

```bash
pip install -e ".[interactive,dev]"
```

#### 4. Verify Installation

```bash
python -c "import flet, matplotlib, pandas, numpy; print('All dependencies installed successfully!')"
```

## Running the Application

### Method 1: Quick Start Script (Easiest)

```bash
./run.sh
```

### Method 2: Direct Python Execution

```bash
python -m app.main
```

### Method 3: With Environment Variables

```bash
FLET_TELEMETRY_DISABLED=1 python -m app.main
```

## First Launch

When you first launch the application:

1. A window will open with two panes:
   - **Left**: Builder sidebar with controls
   - **Right**: Canvas with chart preview

2. The app automatically loads an example:
   - "Overlapping Trends" dataset
   - Multi-series line chart
   - 100 days of time-series data

3. Try the following:
   - Click series visibility toggles
   - Adjust line widths with sliders
   - Change chart type in dropdown
   - Modify title and subtitle
   - Export PNG (click download icon)

## Testing the Installation

Run the test suite to verify everything works:

```bash
# All tests
pytest tests/

# Specific test modules
pytest tests/test_transforms.py
pytest tests/test_serialization.py
pytest tests/test_rendering.py

# With verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=term-missing
```

Expected output:
```
===== test session starts =====
collected 34 items

tests/test_transforms.py .......... [30%]
tests/test_serialization.py .......... [60%]
tests/test_rendering.py .............. [100%]

===== 34 passed in 2.5s =====
```

## Troubleshooting

### Problem: "Module not found" Error

**Solution**: Ensure you're in the correct directory and dependencies are installed

```bash
cd /home/admin/Projects/graph-creator
pip install -e .
```

### Problem: Flet Window Doesn't Open

**Solution**: Check if you have a display server running

```bash
# For headless servers, Flet won't work
# Use on desktop Linux or WSL2 with X server
```

### Problem: Matplotlib Backend Issues

**Solution**: Set the backend explicitly

```bash
export MPLBACKEND=TkAgg  # or Qt5Agg
python -m app.main
```

### Problem: Import Errors with Plotly

**Solution**: Plotly is optional, install it if needed

```bash
pip install plotly kaleido
```

Or use without Plotly (Matplotlib only).

### Problem: Permission Denied on run.sh

**Solution**: Make the script executable

```bash
chmod +x run.sh
```

### Problem: Slow Performance

**Solution**: 
- Reduce dataset size (filter/sample)
- Disable auto-render
- Lower preview DPI
- Limit number of series

## Directory Structure After Installation

```
graph-creator/
├── app/                    # Application code
│   ├── __pycache__/       # Python bytecode (auto-generated)
│   ├── charts/
│   ├── models/
│   ├── services/
│   └── ui/
├── tests/                 # Test suite
├── assets/                # Static assets
├── *.md                   # Documentation
├── pyproject.toml         # Configuration
├── LICENSE                # License file
└── run.sh                 # Start script
```

## Environment Variables

### Disable Telemetry (Recommended)

```bash
export FLET_TELEMETRY_DISABLED=1
```

### Set Matplotlib Backend

```bash
export MPLBACKEND=Agg  # Headless
export MPLBACKEND=TkAgg  # With GUI
```

### Set Log Level

```bash
export LOG_LEVEL=DEBUG  # More verbose
export LOG_LEVEL=INFO   # Default
export LOG_LEVEL=ERROR  # Less verbose
```

## Keyboard Shortcuts

Once running, use these shortcuts:

- **Ctrl+S**: Save project
- **Ctrl+E**: Export image
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+N**: New project

## Next Steps

1. **Read the User Guide**: See `USAGE.md` for detailed features
2. **Try Examples**: Load different example datasets
3. **Import Your Data**: Use CSV/JSON import
4. **Explore Transforms**: Apply data transformations
5. **Customize Charts**: Adjust colors, styles, layouts
6. **Export**: Save high-res PNG/SVG/PDF

## Getting Help

1. Check `USAGE.md` for feature documentation
2. Review `PROJECT_SUMMARY.md` for architecture details
3. Look at example code in `tests/`
4. Check application logs (stdout)

## Uninstallation

To remove the application:

```bash
pip uninstall graph-creator
rm -rf /home/admin/Projects/graph-creator
```

## Update/Reinstall

To update after making changes:

```bash
cd /home/admin/Projects/graph-creator
pip install -e . --force-reinstall --no-deps
```

## Performance Tips

For best performance:
- Use filtered datasets (<10K rows for real-time preview)
- Limit series to 10 or fewer
- Use lower DPI for preview (100)
- Export at high DPI only (300+)
- Disable auto-render for large datasets

## Security Notes

- Application runs 100% offline
- No network requests
- No telemetry when properly configured
- All data stays local
- Safe to use with sensitive data

---

**You're all set!** Run `./run.sh` to start creating charts.


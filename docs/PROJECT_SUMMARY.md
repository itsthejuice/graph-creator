# Graph Creator - Project Summary

## Overview

A fully offline, highly customizable chart creation application built with Flet, Matplotlib, and Pandas. This application runs 100% offline with no telemetry and provides a professional-grade interface for creating publication-quality charts.

## Project Structure

```
graph-creator/
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point
│   │
│   ├── models/                  # Data models and state management
│   │   ├── __init__.py
│   │   ├── data_models.py       # Type-hinted dataclasses for all entities
│   │   └── state.py             # AppState with undo/redo support
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   ├── transforms.py        # Data transformation engine
│   │   ├── data_loader.py       # Data import and example generators
│   │   └── project_io.py        # Save/load project files
│   │
│   ├── charts/                  # Chart rendering engines
│   │   ├── __init__.py
│   │   ├── mpl_renderer.py      # Matplotlib renderer (default)
│   │   └── plotly_renderer.py   # Optional Plotly renderer
│   │
│   └── ui/                      # User interface components
│       ├── __init__.py
│       ├── builder.py           # Left sidebar builder panel
│       ├── canvas.py            # Right pane canvas/preview
│       ├── components.py        # Reusable UI components
│       └── dialogs.py           # Dialog components
│
├── tests/                       # Pytest test suite
│   ├── __init__.py
│   ├── test_transforms.py       # Transform engine tests
│   ├── test_serialization.py   # Project I/O tests
│   └── test_rendering.py        # Chart rendering tests (headless)
│
├── assets/                      # Static assets directory
│
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # Quick start guide
├── USAGE.md                    # Comprehensive user guide
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore patterns
└── run.sh                      # Quick start script

```

## Architecture

### Clean Modular Design

The application follows a clean, layered architecture:

1. **Models Layer** (`app/models/`)
   - Type-hinted dataclasses using Pydantic
   - Immutable data structures with serialization
   - AppState with undo/redo history management
   - Change notification system

2. **Services Layer** (`app/services/`)
   - TransformEngine: 11+ data transformations
   - DataLoader: Multi-format import with type inference
   - ProjectIO: JSON-based project serialization

3. **Charts Layer** (`app/charts/`)
   - MatplotlibRenderer: Production-quality chart generation
   - PlotlyRenderer: Optional interactive preview
   - Headless rendering support (Agg backend)

4. **UI Layer** (`app/ui/`)
   - Builder: Left sidebar with all configuration options
   - Canvas: Right pane with live preview and export
   - Components: Reusable UI elements
   - Dialogs: File pickers and user input

### Key Design Patterns

- **State Management**: Centralized AppState with observer pattern
- **Undo/Redo**: Snapshot-based history (50 levels)
- **Serialization**: Complete project state to/from JSON
- **Separation of Concerns**: Clean layer boundaries
- **Type Safety**: Full type hints throughout

## Features

### Data Sources
- ✅ Import CSV/TSV
- ✅ Import JSON
- ✅ Paste from clipboard
- ✅ Inline spreadsheet editor (via imports)
- ✅ Type inference (numeric, categorical, datetime)
- ✅ Dataset versioning with undo/redo
- ✅ Three built-in examples

### Transforms
- ✅ Column math (add, subtract, multiply, divide)
- ✅ Normalization (min-max, z-score, robust)
- ✅ Smoothing (rolling mean/median, EWM)
- ✅ Time series (resample, interpolate)
- ✅ Rolling operations (mean, median, sum, std, min, max)
- ✅ Difference and percentage change
- ✅ Filter by query
- ✅ Group and aggregate
- ✅ Computed series (NumPy expressions)

### Chart Types
- ✅ Line
- ✅ Area
- ✅ Bar
- ✅ Stacked Bar
- ✅ 100% Bar
- ✅ Scatter
- ✅ Step
- ✅ Histogram
- ✅ KDE (Kernel Density Estimation)
- ✅ Box Plot
- ✅ Violin Plot
- ✅ Multi-series overlay
- ✅ Per-series style controls

### Per-Series Controls
- ✅ Visibility toggle
- ✅ Line width (0.5-5.0)
- ✅ Line style (solid, dashed, dotted, dashdot)
- ✅ Marker style and size
- ✅ Color picker
- ✅ Opacity/alpha
- ✅ Y-axis assignment (primary/secondary)
- ✅ Custom labels

### Axes & Layout
- ✅ Titles and subtitles
- ✅ Legend placement (9 positions)
- ✅ Grid toggles
- ✅ Primary & secondary Y axes
- ✅ Axis scale (linear/log)
- ✅ Axis inversion
- ✅ Custom min/max bounds
- ✅ Axis labels
- ✅ Figure size configuration
- ✅ DPI control

### Annotations
- ✅ Vertical lines
- ✅ Horizontal lines
- ✅ Span (vertical shaded region)
- ✅ Band (horizontal shaded region)
- ✅ Text labels
- ✅ Arrows with labels
- ✅ Reference lines
- ✅ Toggle annotations on/off

### Themes & Branding
- ✅ Light/Dark mode
- ✅ Custom font family
- ✅ Font size control (8-16pt)
- ✅ Title font size
- ✅ Color palette (10 colors)
- ✅ Background color
- ✅ Grid color
- ✅ Text color
- ✅ Theme serialization

### Export & Save
- ✅ Export PNG at custom DPI
- ✅ Export SVG (vector)
- ✅ Export PDF
- ✅ Export data as CSV
- ✅ Export data as JSON
- ✅ Save project (.graphproj)
- ✅ Load project
- ✅ Complete state preservation

### Quick Templates
- ✅ Overlapped Trends (multi-series time-series)
- ✅ Economic Indicators (dual-axis)
- ✅ Contamination vs Rawness (comparative)
- Auto-configured chart settings
- One-click loading

### User Experience
- ✅ Two-pane responsive layout
- ✅ Live preview with auto-render
- ✅ Status bar (rows, render time, warnings)
- ✅ Keyboard shortcuts (Ctrl+S, Ctrl+E, Ctrl+Z, Ctrl+Y, Ctrl+N)
- ✅ Error handling with user-friendly messages
- ✅ Success notifications (snack bars)
- ✅ File picker dialogs
- ✅ Text input dialogs
- ✅ Collapsible sections
- ✅ Labeled controls with tooltips

### Quality & Testing
- ✅ Comprehensive test suite (pytest)
- ✅ Transform engine tests (11 test cases)
- ✅ Serialization tests (6 test cases)
- ✅ Rendering tests (13 test cases)
- ✅ Headless testing (Agg backend)
- ✅ Edge case handling
- ✅ Error recovery
- ✅ Type hints throughout
- ✅ Logging infrastructure

## Dependencies

### Core Dependencies
- **flet** 0.21.2: UI framework
- **matplotlib** 3.8.2: Chart rendering
- **pandas** 2.1.4: Data manipulation
- **numpy** 1.26.2: Numerical operations
- **pydantic** 2.5.3: Data validation
- **scipy** 1.11.4: Scientific computing
- **openpyxl** 3.1.2: Excel support

### Optional Dependencies
- **plotly** 5.18.0: Interactive charts
- **kaleido** 0.2.1: Plotly export

### Development Dependencies
- **pytest** 7.4.3: Testing framework
- **pytest-cov** 4.1.0: Coverage reporting

## Privacy & Offline Operation

### 100% Offline
- ✅ No network requests
- ✅ No telemetry (explicitly disabled)
- ✅ All processing local
- ✅ No external dependencies at runtime

### Data Privacy
- All data stays on local machine
- No cloud storage or sync
- User controls all exports
- Open source and auditable

## Installation & Running

### Quick Start
```bash
cd graph-creator
pip install -e .
./run.sh
```

### Manual Start
```bash
python -m app.main
```

### With Optional Features
```bash
pip install -e ".[interactive]"  # Add Plotly support
pip install -e ".[dev]"          # Add dev tools
```

## Testing

### Run All Tests
```bash
pytest tests/
```

### With Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Individual Test Modules
```bash
pytest tests/test_transforms.py
pytest tests/test_serialization.py
pytest tests/test_rendering.py
```

## Default Example

The application loads an "Overlapping Trends" example by default, demonstrating:
- Multi-series line chart
- Time-series data (100 days)
- Three overlapping metrics
- Sinusoidal patterns with trends
- Proper date axis formatting
- Legend and labels
- Professional styling

This example showcases the primary use case: creating publication-quality overlapping line charts.

## Code Quality

### Type Safety
- All functions have type hints
- Dataclasses for all models
- Pydantic validation where applicable

### Documentation
- Comprehensive docstrings
- Module-level documentation
- User guide (USAGE.md)
- README with quick start

### Error Handling
- Try/except blocks around I/O
- User-friendly error messages
- Logging for debugging
- Graceful degradation

### Performance
- Lazy rendering (auto-render optional)
- Efficient data structures (pandas)
- Memory cleanup (figure.close())
- Limited history (50 snapshots)

## Extensibility

### Adding New Chart Types
1. Add type to ChartConfig Literal
2. Implement rendering in MatplotlibRenderer
3. Add UI dropdown option
4. Write tests

### Adding New Transforms
1. Add method to TransformEngine
2. Add to method_map
3. Create UI controls
4. Write tests

### Adding New Themes
1. Create Theme instance
2. Save as JSON
3. Load on startup
4. Share with users

### Adding New Annotations
1. Add type to Annotation Literal
2. Implement in _add_annotation
3. Create UI dialog
4. Test rendering

## Production Ready

### Stability
- Comprehensive error handling
- Input validation
- Type checking
- Unit tests (30+ cases)

### Usability
- Intuitive UI
- Keyboard shortcuts
- File dialogs
- Status feedback

### Performance
- Fast rendering (<1s typical)
- Efficient data processing
- Memory management
- Progress indicators

### Maintainability
- Clean architecture
- Modular design
- Type hints
- Documentation

## Known Limitations

1. **Large Datasets**: For datasets >100K rows, performance may degrade. Consider aggregation.
2. **Interactive Features**: Plotly integration is optional and requires additional dependencies.
3. **Advanced Annotations**: Complex multi-layer annotations require manual configuration.
4. **Real-time Data**: No live data streaming; import/refresh workflow.
5. **3D Charts**: Only 2D visualizations supported.

## Future Enhancements (Not Implemented)

- Real-time data streaming
- 3D surface plots
- Animation/GIF export
- Multi-page PDF reports
- Database connectors
- REST API
- Plugin system
- Collaborative editing

## Support & Contribution

### Getting Help
1. Read USAGE.md
2. Check examples
3. Review test cases
4. Check logs

### Contributing
1. Fork repository
2. Create feature branch
3. Write tests
4. Submit PR

### Reporting Issues
Include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Data sample (if applicable)
- Logs/error messages

## License

MIT License - See LICENSE file

## Credits

Built with:
- Flet (Python UI framework)
- Matplotlib (industry-standard charting)
- Pandas (data manipulation)
- NumPy (numerical computing)
- SciPy (scientific computing)

## Version

1.0.0 - Initial Release

---

**Graph Creator** - Professional chart creation, completely offline.


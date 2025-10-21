# Graph Creator

A fully offline, highly customizable chart creation application built with Flet and Matplotlib.

## Features

- **Data Sources**: Import CSV/TSV/JSON, paste from clipboard, or use inline spreadsheet editor
- **Transforms**: Column math, normalization, smoothing, resampling, filtering, grouping
- **Chart Types**: Line, area, bar, scatter, histogram, KDE, box plots, and more
- **Customization**: Dual Y-axes, annotations, themes, custom colors and fonts
- **Export**: PNG/SVG/PDF at custom DPI, save/load project files
- **Templates**: Quick-start templates for common chart types
- **100% Offline**: No telemetry or external dependencies

## Installation

```bash
# Clone or navigate to the project directory
cd graph-creator

# Install dependencies
pip install -e .

# Optional: Install interactive Plotly support
pip install -e ".[interactive]"

# Optional: Install development dependencies
pip install -e ".[dev]"
```

## Running the Application

```bash
python -m app.main
```

## Keyboard Shortcuts

- **Ctrl+Z / Ctrl+Y**: Undo/Redo
- **Ctrl+S**: Save project
- **Ctrl+E**: Export image
- **Ctrl+N**: New project

## Testing

```bash
pytest tests/
```

## Project Structure

```
graph-creator/
├── app/
│   ├── main.py           # Application entry point
│   ├── models/           # Data models and state
│   ├── ui/               # UI components
│   ├── services/         # Business logic (transforms, I/O)
│   └── charts/           # Chart renderers
├── tests/                # Unit tests
├── assets/               # Static assets
├── pyproject.toml        # Project configuration
└── README.md             # This file
```

## Architecture

The application follows a clean, modular architecture:

- **UI Layer** (`app/ui/`): Flet-based user interface components
- **Models** (`app/models/`): Type-hinted dataclasses for state management
- **Services** (`app/services/`): Transform engine, data loading, project I/O
- **Charts** (`app/charts/`): Matplotlib and optional Plotly renderers

## License

MIT


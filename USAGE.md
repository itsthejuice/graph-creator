# Graph Creator - User Guide

## Getting Started

### Installation

```bash
cd graph-creator
pip install -e .
```

### Running the Application

```bash
# Method 1: Using the run script
./run.sh

# Method 2: Direct Python execution
python -m app.main

# Method 3: With telemetry disabled
FLET_TELEMETRY_DISABLED=1 python -m app.main
```

## Features Overview

### 1. Data Sources

#### Loading Example Data
- Click the lightbulb icon (💡) in the Data Sources section
- Choose from:
  - **Overlapping Trends**: Multi-series time-series data with overlapping patterns
  - **Economic Indicators**: Dual-axis economic data (GDP, unemployment, interest rates)
  - **Contamination vs Rawness**: Sample-based comparative analysis

#### Importing Your Data
- Click the upload icon (📤) in the Data Sources section
- Options:
  - **Import CSV**: Standard comma-separated values
  - **Import JSON**: JSON array format
  - **Paste from Clipboard**: Copy data from Excel, Google Sheets, etc.

### 2. Chart Types

Available chart types:
- **Line**: Standard line charts for trends
- **Area**: Filled area charts
- **Bar**: Side-by-side bar charts
- **Stacked Bar**: Stacked bar visualization
- **100% Bar**: Normalized percentage stacks
- **Scatter**: Point-based scatter plots
- **Step**: Step function visualization
- **Histogram**: Distribution analysis
- **KDE**: Kernel Density Estimation
- **Box Plot**: Statistical distribution boxes
- **Violin Plot**: Distribution with density

### 3. Series Configuration

#### X Column
Select which column to use as the X-axis (typically time or categories)

#### Per-Series Controls
For each data series, you can configure:
- **Visibility**: Toggle series on/off
- **Line Width**: Adjust thickness (0.5 - 5.0)
- **Line Style**: Solid, Dashed, Dotted, Dash-Dot
- **Y Axis**: Assign to Primary or Secondary Y-axis
- **Color**: Custom color selection
- **Opacity**: Transparency level

### 4. Axes & Scales

#### Primary Y Axis
- **Label**: Custom axis label
- **Scale**: Linear or Logarithmic
- **Grid**: Toggle grid lines
- **Min/Max**: Set axis bounds

#### Secondary Y Axis
- Enable by assigning a series to "Secondary" axis
- Same configuration options as primary

### 5. Layout & Labels

- **Title**: Main chart title
- **Subtitle**: Secondary descriptive text
- **Legend Position**: Best, Upper Right, Upper Left, Lower Left, Lower Right, None
- **Figure Size**: Adjust width and height
- **DPI**: Resolution for exports

### 6. Annotations

Add visual markers to your chart:
- **Horizontal Line**: Reference line at Y value
- **Vertical Line**: Reference line at X value
- **Span**: Shaded region between two points
- **Text**: Custom text labels
- **Arrow**: Annotated arrows
- **Band**: Horizontal shaded band

### 7. Theme & Styling

- **Mode**: Light or Dark theme
- **Font Size**: Adjust overall text size (8-16pt)
- **Font Family**: Choose font (default: sans-serif)
- **Color Palette**: Custom color schemes

### 8. Data Transformations

Apply transformations to your data:

#### Column Math
- Add, subtract, multiply, or divide columns
- Create computed columns

#### Normalization
- **Min-Max**: Scale to 0-1 range
- **Z-Score**: Standardize to mean=0, std=1
- **Robust**: IQR-based normalization

#### Smoothing
- **Rolling Mean**: Moving average
- **Rolling Median**: Moving median
- **EWM**: Exponentially weighted moving average

#### Time Series
- **Resample**: Aggregate by time period (D, W, M, Y)
- **Interpolate**: Fill missing values
- **Diff**: Calculate differences
- **Pct Change**: Calculate percentage changes

#### Filtering & Grouping
- **Filter**: Query-based row filtering
- **Group**: Group and aggregate data

## Keyboard Shortcuts

- **Ctrl+S**: Save project
- **Ctrl+E**: Export image
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+N**: New project

## Export Options

### Image Export
- **PNG**: Raster format (default 300 DPI)
- **SVG**: Vector format (scalable)
- **PDF**: Document format

### Data Export
- **CSV**: Export transformed data

### Project Files
- **Save Project**: Save as `.graphproj` file
- **Load Project**: Restore complete project state
- Project files include:
  - Dataset
  - All transformations
  - Chart configuration
  - Theme settings
  - Annotations

## Tips & Best Practices

### Creating Overlapping Line Charts

1. Load example data or import your time-series data
2. Select "Line" chart type
3. Choose date/time column as X axis
4. Multiple numeric columns will auto-populate as series
5. Adjust line width, style, and colors for each series
6. Use secondary Y-axis for different scales
7. Add reference lines or annotations

### Multi-Axis Charts

1. Configure multiple series
2. Assign some series to "Secondary" Y-axis
3. Different scales will be applied automatically
4. Useful for comparing metrics with different units (e.g., GDP vs. %)

### Data Preparation

1. Import raw data
2. Apply transformations in order:
   - Filter invalid rows
   - Interpolate missing values
   - Normalize if comparing different scales
   - Smooth to reduce noise
3. Use "Computed Series" for custom calculations
4. Each transformation can be toggled on/off

### Theme Customization

1. Start with Light/Dark mode
2. Adjust font size for readability
3. Customize color palette for brand consistency
4. Save as project template

### Performance Tips

- Limit displayed series to 10 or fewer
- For large datasets, apply filtering/grouping first
- Use lower DPI (100) for preview, high DPI (300+) for export
- Enable "Auto Render" cautiously with large data

## Troubleshooting

### Chart Not Rendering
- Verify data is loaded (check status bar)
- Ensure X column is selected
- Check that series columns exist in data
- Review warnings in status bar

### Series Not Visible
- Check series visibility toggles
- Verify data is numeric (non-numeric ignored)
- Check if series is on correct axis
- Look for scale issues (try log scale)

### Export Issues
- Ensure chart renders successfully first
- Check file permissions for save location
- For SVG/PDF, ensure matplotlib backend is configured
- Try PNG export if other formats fail

### Import Errors
- Verify CSV has headers
- Check JSON is array format: `[{...}, {...}]`
- Ensure clipboard data is tab or comma separated
- Try explicit file format selection

## Advanced Features

### Expression Editor
Use Python/NumPy syntax for computed series:
```python
# Simple arithmetic
A * 2 + B

# NumPy functions
np.sqrt(A)
np.log(B + 1)

# Pandas operations
A.rolling(7).mean()
```

### Custom Annotations
Combine multiple annotation types:
- Add vertical lines for key events
- Add horizontal reference lines (e.g., target values)
- Use text annotations for explanations
- Create visual bands for time periods

### Workflow Automation
1. Create template project with:
   - Standard theme
   - Common annotations
   - Default transformations
2. Save as `.graphproj`
3. Load and replace data for consistent styling

## Example Workflows

### Overlapping Trends Analysis
1. Load "Overlapping Trends" example
2. Chart type: Line
3. X column: Date
4. All metrics visible
5. Adjust colors for clarity
6. Add moving average annotations
7. Export PNG at 300 DPI

### Before/After Comparison
1. Import data with two time periods
2. Use vertical line to mark transition
3. Different colors for before/after
4. Add text annotation explaining change
5. Use area chart for visual impact

### Multi-Metric Dashboard
1. Import data with multiple metrics
2. Group related metrics on same axis
3. Use secondary axis for different scales
4. Add reference lines for targets
5. Custom title and subtitle
6. Export high-res PDF

## API Reference

See module documentation:
- `app.models.data_models`: Data structures
- `app.services.transforms`: Transform engine
- `app.charts.mpl_renderer`: Matplotlib renderer
- `app.services.project_io`: File I/O

## Support

For issues or questions:
1. Check this guide
2. Review example projects
3. Check console for error messages
4. Verify all dependencies installed

## License

MIT License - See LICENSE file


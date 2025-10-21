"""Optional Plotly-based interactive chart renderer."""

from __future__ import annotations

from typing import Optional, Tuple, Dict, Any
import pandas as pd

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    go = None
    make_subplots = None

from ..models.data_models import ChartConfig, Theme


class PlotlyRenderer:
    """Renders interactive charts using Plotly."""
    
    def __init__(self):
        if not PLOTLY_AVAILABLE:
            raise ImportError("Plotly is not installed. Install with: pip install plotly")
        self.figure: Optional[go.Figure] = None
    
    def render(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        theme: Theme,
    ) -> Tuple[go.Figure, Dict[str, Any]]:
        """Render interactive chart."""
        import time
        start_time = time.time()
        
        warnings = []
        
        # Check if we need secondary axis
        has_secondary = any(
            s.y_axis == "secondary" and s.visible 
            for s in config.series_styles
        )
        
        # Create figure
        if has_secondary:
            fig = make_subplots(specs=[[{"secondary_y": True}]])
        else:
            fig = go.Figure()
        
        # Add traces
        if config.chart_type in ["line", "area", "scatter"]:
            warnings = self._add_xy_traces(df, config, fig, has_secondary, theme)
        
        # Update layout
        fig.update_layout(
            title=config.title,
            xaxis_title=config.x_axis.label,
            yaxis_title=config.y_axis_primary.label,
            template="plotly_dark" if theme.mode == "dark" else "plotly_white",
            font=dict(family=theme.font_family, size=theme.font_size),
            showlegend=config.show_legend,
            width=config.figure_width * 100,
            height=config.figure_height * 100,
        )
        
        # Calculate render time
        render_time = time.time() - start_time
        
        metadata = {
            "render_time": render_time,
            "warnings": warnings,
            "rows": len(df),
        }
        
        self.figure = fig
        return fig, metadata
    
    def _add_xy_traces(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        fig: go.Figure,
        has_secondary: bool,
        theme: Theme,
    ) -> list:
        """Add XY traces to figure."""
        warnings = []
        
        if not config.x_column or config.x_column not in df.columns:
            warnings.append("X column not specified or not found")
            return warnings
        
        x_data = df[config.x_column]
        
        for i, series_style in enumerate(config.series_styles):
            if not series_style.visible:
                continue
            
            if series_style.column not in df.columns:
                continue
            
            y_data = df[series_style.column]
            
            if not pd.api.types.is_numeric_dtype(y_data):
                continue
            
            color = series_style.color if series_style.color else theme.color_palette[i % len(theme.color_palette)]
            label = series_style.label if series_style.label else series_style.column
            
            # Determine trace type
            if config.chart_type == "line":
                trace = go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='lines' if not series_style.marker else 'lines+markers',
                    name=label,
                    line=dict(
                        color=color,
                        width=series_style.line_width,
                    ),
                    opacity=series_style.alpha,
                )
            elif config.chart_type == "area":
                trace = go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='lines',
                    name=label,
                    fill='tonexty' if i > 0 else 'tozeroy',
                    line=dict(color=color),
                    opacity=series_style.alpha,
                )
            elif config.chart_type == "scatter":
                trace = go.Scatter(
                    x=x_data,
                    y=y_data,
                    mode='markers',
                    name=label,
                    marker=dict(
                        color=color,
                        size=series_style.marker_size,
                    ),
                    opacity=series_style.alpha,
                )
            else:
                continue
            
            # Add trace
            if has_secondary and series_style.y_axis == "secondary":
                fig.add_trace(trace, secondary_y=True)
            else:
                if has_secondary:
                    fig.add_trace(trace, secondary_y=False)
                else:
                    fig.add_trace(trace)
        
        return warnings
    
    def to_html(self) -> str:
        """Export figure to HTML."""
        if self.figure is None:
            return ""
        
        return self.figure.to_html()
    
    def save_to_file(self, file_path: str) -> None:
        """Save figure to file."""
        if self.figure is None:
            return
        
        if file_path.endswith('.html'):
            self.figure.write_html(file_path)
        else:
            # Requires kaleido
            self.figure.write_image(file_path)


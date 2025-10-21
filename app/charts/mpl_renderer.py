"""Matplotlib-based chart renderer."""

import io
from typing import Optional, Tuple
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy import stats

from ..models.data_models import ChartConfig, SeriesStyle, Theme, Annotation


class MatplotlibRenderer:
    """Renders charts using Matplotlib."""
    
    def __init__(self):
        self.figure: Optional[Figure] = None
    
    def render(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        theme: Theme,
    ) -> Tuple[Figure, dict]:
        """Render chart and return figure and metadata."""
        import time
        start_time = time.time()
        
        # Apply theme
        self._apply_theme(theme)
        
        # Create figure
        fig = plt.figure(
            figsize=(config.figure_width, config.figure_height),
            dpi=config.dpi,
        )
        
        # Create axes
        ax1 = fig.add_subplot(111)
        ax2 = None
        
        # Check if we need secondary axis
        has_secondary = any(
            s.y_axis == "secondary" and s.visible 
            for s in config.series_styles
        )
        
        if has_secondary and config.y_axis_secondary:
            ax2 = ax1.twinx()
        
        # Render based on chart type
        warnings = []
        
        if config.chart_type in ["line", "area", "scatter", "step"]:
            warnings = self._render_xy_chart(df, config, ax1, ax2, theme)
        elif config.chart_type in ["bar", "stacked_bar", "bar_100"]:
            warnings = self._render_bar_chart(df, config, ax1, theme)
        elif config.chart_type == "histogram":
            warnings = self._render_histogram(df, config, ax1, theme)
        elif config.chart_type == "kde":
            warnings = self._render_kde(df, config, ax1, theme)
        elif config.chart_type in ["box", "violin"]:
            warnings = self._render_distribution(df, config, ax1, theme)
        
        # Set titles
        if config.title:
            title_y = 1.02 if config.subtitle else 1.0
            ax1.set_title(
                config.title,
                fontsize=theme.title_font_size,
                fontweight='bold',
                pad=30 if config.subtitle else 20,
                y=title_y,
            )
        
        if config.subtitle:
            fig.text(
                0.5, 0.98,
                config.subtitle,
                ha='center',
                fontsize=theme.font_size - 1,
                style='italic',
                color=theme.text_color,
                alpha=0.8,
            )
        
        # Configure axes
        self._configure_axis(ax1, config.x_axis, config.y_axis_primary, "primary")
        
        if ax2 and config.y_axis_secondary:
            self._configure_secondary_axis(ax2, config.y_axis_secondary)
        
        # Add legend
        if config.show_legend and config.legend_position != "none":
            handles1, labels1 = ax1.get_legend_handles_labels()
            handles2, labels2 = [], []
            
            if ax2:
                handles2, labels2 = ax2.get_legend_handles_labels()
            
            all_handles = handles1 + handles2
            all_labels = labels1 + labels2
            
            if all_handles:
                ax1.legend(
                    all_handles,
                    all_labels,
                    loc=config.legend_position,
                    framealpha=0.9,
                )
        
        # Add annotations
        for annotation in config.annotations:
            if annotation.enabled:
                self._add_annotation(ax1, annotation)
        
        # Tight layout
        fig.tight_layout()
        
        # Calculate render time
        render_time = time.time() - start_time
        
        # Metadata
        metadata = {
            "render_time": render_time,
            "warnings": warnings,
            "rows": len(df),
        }
        
        self.figure = fig
        return fig, metadata
    
    def _apply_theme(self, theme: Theme) -> None:
        """Apply theme to matplotlib."""
        if theme.mode == "dark":
            plt.style.use('dark_background')
        else:
            plt.style.use('default')
        
        # Set font
        plt.rcParams['font.family'] = theme.font_family
        plt.rcParams['font.size'] = theme.font_size
        
        # Set colors
        plt.rcParams['axes.facecolor'] = theme.background_color
        plt.rcParams['figure.facecolor'] = theme.background_color
        plt.rcParams['text.color'] = theme.text_color
        plt.rcParams['axes.labelcolor'] = theme.text_color
        plt.rcParams['xtick.color'] = theme.text_color
        plt.rcParams['ytick.color'] = theme.text_color
        plt.rcParams['grid.color'] = theme.grid_color
        
        # Set color cycle
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=theme.color_palette)
    
    def _render_xy_chart(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        ax1,
        ax2,
        theme: Theme,
    ) -> list:
        """Render line, area, scatter, or step chart."""
        warnings = []
        
        if not config.x_column or config.x_column not in df.columns:
            warnings.append("X column not specified or not found")
            return warnings
        
        x_data = df[config.x_column]
        
        # Plot each series
        for i, series_style in enumerate(config.series_styles):
            if not series_style.visible:
                continue
            
            if series_style.column not in df.columns:
                warnings.append(f"Column '{series_style.column}' not found")
                continue
            
            y_data = df[series_style.column]
            
            # Skip if not numeric
            if not pd.api.types.is_numeric_dtype(y_data):
                warnings.append(f"Column '{series_style.column}' is not numeric")
                continue
            
            # Select axis
            ax = ax2 if series_style.y_axis == "secondary" and ax2 else ax1
            
            # Get style parameters
            color = series_style.color if series_style.color else theme.color_palette[i % len(theme.color_palette)]
            label = series_style.label if series_style.label else series_style.column
            
            linestyle_map = {
                "solid": "-",
                "dashed": "--",
                "dotted": ":",
                "dashdot": "-.",
            }
            linestyle = linestyle_map.get(series_style.line_style, "-")
            
            # Plot based on chart type
            if config.chart_type == "line":
                ax.plot(
                    x_data, y_data,
                    label=label,
                    color=color,
                    linewidth=series_style.line_width,
                    linestyle=linestyle,
                    marker=series_style.marker if series_style.marker else None,
                    markersize=series_style.marker_size,
                    alpha=series_style.alpha,
                )
            elif config.chart_type == "area":
                ax.fill_between(
                    x_data, y_data,
                    label=label,
                    color=color,
                    alpha=series_style.alpha * 0.5,
                )
                ax.plot(
                    x_data, y_data,
                    color=color,
                    linewidth=series_style.line_width,
                    linestyle=linestyle,
                )
            elif config.chart_type == "scatter":
                ax.scatter(
                    x_data, y_data,
                    label=label,
                    color=color,
                    s=series_style.marker_size ** 2,
                    alpha=series_style.alpha,
                    marker=series_style.marker if series_style.marker else 'o',
                )
            elif config.chart_type == "step":
                ax.step(
                    x_data, y_data,
                    label=label,
                    color=color,
                    linewidth=series_style.line_width,
                    linestyle=linestyle,
                    where='mid',
                    alpha=series_style.alpha,
                )
        
        return warnings
    
    def _render_bar_chart(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        ax,
        theme: Theme,
    ) -> list:
        """Render bar chart."""
        warnings = []
        
        if not config.x_column or config.x_column not in df.columns:
            warnings.append("X column not specified or not found")
            return warnings
        
        x_data = df[config.x_column]
        
        # Get visible numeric series
        series_data = []
        series_labels = []
        series_colors = []
        
        for i, series_style in enumerate(config.series_styles):
            if not series_style.visible:
                continue
            
            if series_style.column not in df.columns:
                continue
            
            y_data = df[series_style.column]
            
            if not pd.api.types.is_numeric_dtype(y_data):
                continue
            
            series_data.append(y_data)
            series_labels.append(series_style.label if series_style.label else series_style.column)
            series_colors.append(
                series_style.color if series_style.color 
                else theme.color_palette[i % len(theme.color_palette)]
            )
        
        if not series_data:
            warnings.append("No numeric data to plot")
            return warnings
        
        # Plot bars
        x_pos = np.arange(len(x_data))
        
        if config.chart_type == "bar":
            width = 0.8 / len(series_data)
            for i, (data, label, color) in enumerate(zip(series_data, series_labels, series_colors)):
                offset = (i - len(series_data) / 2) * width + width / 2
                ax.bar(
                    x_pos + offset,
                    data,
                    width=width,
                    label=label,
                    color=color,
                )
        elif config.chart_type == "stacked_bar":
            bottom = np.zeros(len(x_data))
            for data, label, color in zip(series_data, series_labels, series_colors):
                ax.bar(
                    x_pos,
                    data,
                    label=label,
                    color=color,
                    bottom=bottom,
                )
                bottom += data
        elif config.chart_type == "bar_100":
            # Normalize to 100%
            total = sum(series_data)
            bottom = np.zeros(len(x_data))
            for data, label, color in zip(series_data, series_labels, series_colors):
                normalized = (data / total) * 100
                ax.bar(
                    x_pos,
                    normalized,
                    label=label,
                    color=color,
                    bottom=bottom,
                )
                bottom += normalized
            ax.set_ylabel("Percentage (%)")
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_data, rotation=45, ha='right')
        
        return warnings
    
    def _render_histogram(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        ax,
        theme: Theme,
    ) -> list:
        """Render histogram."""
        warnings = []
        
        for i, series_style in enumerate(config.series_styles):
            if not series_style.visible:
                continue
            
            if series_style.column not in df.columns:
                continue
            
            data = df[series_style.column].dropna()
            
            if not pd.api.types.is_numeric_dtype(data):
                continue
            
            color = series_style.color if series_style.color else theme.color_palette[i % len(theme.color_palette)]
            label = series_style.label if series_style.label else series_style.column
            
            ax.hist(
                data,
                bins=30,
                label=label,
                color=color,
                alpha=series_style.alpha,
                edgecolor='black',
            )
        
        ax.set_ylabel("Frequency")
        
        return warnings
    
    def _render_kde(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        ax,
        theme: Theme,
    ) -> list:
        """Render KDE (Kernel Density Estimate) plot."""
        warnings = []
        
        for i, series_style in enumerate(config.series_styles):
            if not series_style.visible:
                continue
            
            if series_style.column not in df.columns:
                continue
            
            data = df[series_style.column].dropna()
            
            if not pd.api.types.is_numeric_dtype(data):
                continue
            
            if len(data) < 2:
                warnings.append(f"Not enough data points for KDE in '{series_style.column}'")
                continue
            
            color = series_style.color if series_style.color else theme.color_palette[i % len(theme.color_palette)]
            label = series_style.label if series_style.label else series_style.column
            
            # Calculate KDE
            try:
                kde = stats.gaussian_kde(data)
                x_range = np.linspace(data.min(), data.max(), 200)
                y_kde = kde(x_range)
                
                ax.plot(
                    x_range,
                    y_kde,
                    label=label,
                    color=color,
                    linewidth=series_style.line_width,
                    alpha=series_style.alpha,
                )
                ax.fill_between(
                    x_range,
                    y_kde,
                    alpha=series_style.alpha * 0.3,
                    color=color,
                )
            except Exception as e:
                warnings.append(f"KDE error for '{series_style.column}': {str(e)}")
        
        ax.set_ylabel("Density")
        
        return warnings
    
    def _render_distribution(
        self,
        df: pd.DataFrame,
        config: ChartConfig,
        ax,
        theme: Theme,
    ) -> list:
        """Render box or violin plot."""
        warnings = []
        
        data_list = []
        labels = []
        colors = []
        
        for i, series_style in enumerate(config.series_styles):
            if not series_style.visible:
                continue
            
            if series_style.column not in df.columns:
                continue
            
            data = df[series_style.column].dropna()
            
            if not pd.api.types.is_numeric_dtype(data):
                continue
            
            data_list.append(data)
            labels.append(series_style.label if series_style.label else series_style.column)
            colors.append(
                series_style.color if series_style.color 
                else theme.color_palette[i % len(theme.color_palette)]
            )
        
        if not data_list:
            warnings.append("No numeric data to plot")
            return warnings
        
        if config.chart_type == "box":
            bp = ax.boxplot(
                data_list,
                labels=labels,
                patch_artist=True,
            )
            for patch, color in zip(bp['boxes'], colors):
                patch.set_facecolor(color)
        elif config.chart_type == "violin":
            vp = ax.violinplot(
                data_list,
                showmeans=True,
                showmedians=True,
            )
            for i, pc in enumerate(vp['bodies']):
                pc.set_facecolor(colors[i % len(colors)])
                pc.set_alpha(0.7)
            ax.set_xticks(np.arange(1, len(labels) + 1))
            ax.set_xticklabels(labels)
        
        return warnings
    
    def _configure_axis(self, ax, x_config, y_config, axis_type: str) -> None:
        """Configure axis properties."""
        # X axis
        if x_config.label:
            ax.set_xlabel(x_config.label)
        
        if x_config.scale == "log":
            ax.set_xscale('log')
        
        if x_config.invert:
            ax.invert_xaxis()
        
        if x_config.min_value is not None or x_config.max_value is not None:
            xlim = list(ax.get_xlim())
            if x_config.min_value is not None:
                xlim[0] = x_config.min_value
            if x_config.max_value is not None:
                xlim[1] = x_config.max_value
            ax.set_xlim(xlim)
        
        # Y axis
        if y_config.label:
            ax.set_ylabel(y_config.label)
        
        if y_config.scale == "log":
            ax.set_yscale('log')
        
        if y_config.invert:
            ax.invert_yaxis()
        
        if y_config.min_value is not None or y_config.max_value is not None:
            ylim = list(ax.get_ylim())
            if y_config.min_value is not None:
                ylim[0] = y_config.min_value
            if y_config.max_value is not None:
                ylim[1] = y_config.max_value
            ax.set_ylim(ylim)
        
        # Grid
        if y_config.show_grid:
            ax.grid(True, alpha=0.3)
        else:
            ax.grid(False)
    
    def _configure_secondary_axis(self, ax, y_config) -> None:
        """Configure secondary Y axis."""
        if y_config.label:
            ax.set_ylabel(y_config.label)
        
        if y_config.scale == "log":
            ax.set_yscale('log')
        
        if y_config.invert:
            ax.invert_yaxis()
        
        if y_config.min_value is not None or y_config.max_value is not None:
            ylim = list(ax.get_ylim())
            if y_config.min_value is not None:
                ylim[0] = y_config.min_value
            if y_config.max_value is not None:
                ylim[1] = y_config.max_value
            ax.set_ylim(ylim)
    
    def _add_annotation(self, ax, annotation: Annotation) -> None:
        """Add annotation to chart."""
        params = annotation.params
        
        if annotation.annotation_type == "vline":
            x = params.get("x", 0)
            label = params.get("label", "")
            color = params.get("color", "red")
            linestyle = params.get("linestyle", "--")
            ax.axvline(x=x, color=color, linestyle=linestyle, alpha=0.7, label=label)
        
        elif annotation.annotation_type == "hline":
            y = params.get("y", 0)
            label = params.get("label", "")
            color = params.get("color", "red")
            linestyle = params.get("linestyle", "--")
            ax.axhline(y=y, color=color, linestyle=linestyle, alpha=0.7, label=label)
        
        elif annotation.annotation_type == "span":
            xmin = params.get("xmin", 0)
            xmax = params.get("xmax", 1)
            color = params.get("color", "yellow")
            ax.axvspan(xmin, xmax, alpha=0.2, color=color)
        
        elif annotation.annotation_type == "text":
            x = params.get("x", 0)
            y = params.get("y", 0)
            text = params.get("text", "")
            fontsize = params.get("fontsize", 10)
            ax.text(x, y, text, fontsize=fontsize, bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5))
        
        elif annotation.annotation_type == "arrow":
            x = params.get("x", 0)
            y = params.get("y", 0)
            dx = params.get("dx", 0)
            dy = params.get("dy", 0)
            text = params.get("text", "")
            ax.annotate(
                text, xy=(x, y), xytext=(x + dx, y + dy),
                arrowprops=dict(arrowstyle="->", color="black"),
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
            )
        
        elif annotation.annotation_type == "band":
            ymin = params.get("ymin", 0)
            ymax = params.get("ymax", 1)
            color = params.get("color", "gray")
            ax.axhspan(ymin, ymax, alpha=0.2, color=color)
    
    def save_to_bytes(self, format: str = "png", dpi: int = 100) -> bytes:
        """Save figure to bytes."""
        if self.figure is None:
            return b""
        
        buf = io.BytesIO()
        self.figure.savefig(buf, format=format, dpi=dpi, bbox_inches='tight')
        buf.seek(0)
        return buf.read()
    
    def save_to_file(self, file_path: str, dpi: int = 100) -> None:
        """Save figure to file."""
        if self.figure is None:
            return
        
        self.figure.savefig(file_path, dpi=dpi, bbox_inches='tight')
    
    def close(self) -> None:
        """Close figure and free memory."""
        if self.figure is not None:
            plt.close(self.figure)
            self.figure = None


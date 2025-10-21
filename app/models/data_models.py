"""Data models for the graph creator application."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Literal
from datetime import datetime
import pandas as pd


@dataclass
class DataSource:
    """Represents a data source with its metadata."""
    
    name: str
    df: pd.DataFrame
    source_type: Literal["csv", "json", "clipboard", "manual"] = "manual"
    created_at: datetime = field(default_factory=datetime.now)
    version: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "data": self.df.to_dict(orient="split"),
            "source_type": self.source_type,
            "created_at": self.created_at.isoformat(),
            "version": self.version,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataSource":
        """Deserialize from dictionary."""
        df = pd.DataFrame(**data["data"])
        return cls(
            name=data["name"],
            df=df,
            source_type=data["source_type"],
            created_at=datetime.fromisoformat(data["created_at"]),
            version=data["version"],
        )


@dataclass
class Transform:
    """Represents a data transformation."""
    
    transform_type: str
    params: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "transform_type": self.transform_type,
            "params": self.params,
            "enabled": self.enabled,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transform":
        """Deserialize from dictionary."""
        return cls(**data)


@dataclass
class SeriesStyle:
    """Style configuration for a single series."""
    
    column: str
    visible: bool = True
    line_width: float = 2.0
    line_style: Literal["solid", "dashed", "dotted", "dashdot"] = "solid"
    marker: str = ""
    marker_size: float = 6.0
    color: Optional[str] = None
    alpha: float = 1.0
    y_axis: Literal["primary", "secondary"] = "primary"
    label: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "column": self.column,
            "visible": self.visible,
            "line_width": self.line_width,
            "line_style": self.line_style,
            "marker": self.marker,
            "marker_size": self.marker_size,
            "color": self.color,
            "alpha": self.alpha,
            "y_axis": self.y_axis,
            "label": self.label,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SeriesStyle":
        """Deserialize from dictionary."""
        return cls(**data)


@dataclass
class AxisConfig:
    """Axis configuration."""
    
    label: str = ""
    scale: Literal["linear", "log"] = "linear"
    show_grid: bool = True
    invert: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "label": self.label,
            "scale": self.scale,
            "show_grid": self.show_grid,
            "invert": self.invert,
            "min_value": self.min_value,
            "max_value": self.max_value,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AxisConfig":
        """Deserialize from dictionary."""
        return cls(**data)


@dataclass
class Annotation:
    """Chart annotation."""
    
    annotation_type: Literal["vline", "hline", "span", "text", "arrow", "band"]
    params: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "annotation_type": self.annotation_type,
            "params": self.params,
            "enabled": self.enabled,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Annotation":
        """Deserialize from dictionary."""
        return cls(**data)


@dataclass
class Theme:
    """Visual theme configuration."""
    
    name: str = "default"
    mode: Literal["light", "dark"] = "light"
    font_family: str = "sans-serif"
    font_size: float = 11.0
    title_font_size: float = 14.0
    color_palette: List[str] = field(default_factory=lambda: [
        "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
        "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
    ])
    background_color: str = "#ffffff"
    grid_color: str = "#e0e0e0"
    text_color: str = "#000000"
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "mode": self.mode,
            "font_family": self.font_family,
            "font_size": self.font_size,
            "title_font_size": self.title_font_size,
            "color_palette": self.color_palette,
            "background_color": self.background_color,
            "grid_color": self.grid_color,
            "text_color": self.text_color,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theme":
        """Deserialize from dictionary."""
        return cls(**data)


@dataclass
class ChartConfig:
    """Complete chart configuration."""
    
    chart_type: Literal[
        "line", "area", "bar", "stacked_bar", "bar_100", 
        "scatter", "step", "histogram", "kde", "box", "violin"
    ] = "line"
    title: str = ""
    subtitle: str = ""
    x_column: Optional[str] = None
    series_styles: List[SeriesStyle] = field(default_factory=list)
    x_axis: AxisConfig = field(default_factory=AxisConfig)
    y_axis_primary: AxisConfig = field(default_factory=AxisConfig)
    y_axis_secondary: Optional[AxisConfig] = None
    legend_position: Literal["best", "upper right", "upper left", "lower left", 
                              "lower right", "right", "center", "none"] = "best"
    show_legend: bool = True
    annotations: List[Annotation] = field(default_factory=list)
    figure_width: float = 10.0
    figure_height: float = 6.0
    dpi: int = 100
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "chart_type": self.chart_type,
            "title": self.title,
            "subtitle": self.subtitle,
            "x_column": self.x_column,
            "series_styles": [s.to_dict() for s in self.series_styles],
            "x_axis": self.x_axis.to_dict(),
            "y_axis_primary": self.y_axis_primary.to_dict(),
            "y_axis_secondary": self.y_axis_secondary.to_dict() if self.y_axis_secondary else None,
            "legend_position": self.legend_position,
            "show_legend": self.show_legend,
            "annotations": [a.to_dict() for a in self.annotations],
            "figure_width": self.figure_width,
            "figure_height": self.figure_height,
            "dpi": self.dpi,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChartConfig":
        """Deserialize from dictionary."""
        return cls(
            chart_type=data["chart_type"],
            title=data["title"],
            subtitle=data["subtitle"],
            x_column=data["x_column"],
            series_styles=[SeriesStyle.from_dict(s) for s in data["series_styles"]],
            x_axis=AxisConfig.from_dict(data["x_axis"]),
            y_axis_primary=AxisConfig.from_dict(data["y_axis_primary"]),
            y_axis_secondary=AxisConfig.from_dict(data["y_axis_secondary"]) if data["y_axis_secondary"] else None,
            legend_position=data["legend_position"],
            show_legend=data["show_legend"],
            annotations=[Annotation.from_dict(a) for a in data["annotations"]],
            figure_width=data["figure_width"],
            figure_height=data["figure_height"],
            dpi=data["dpi"],
        )


@dataclass
class ProjectState:
    """Complete project state for serialization."""
    
    data_source: Optional[DataSource] = None
    transforms: List[Transform] = field(default_factory=list)
    chart_config: ChartConfig = field(default_factory=ChartConfig)
    theme: Theme = field(default_factory=Theme)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "data_source": self.data_source.to_dict() if self.data_source else None,
            "transforms": [t.to_dict() for t in self.transforms],
            "chart_config": self.chart_config.to_dict(),
            "theme": self.theme.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProjectState":
        """Deserialize from dictionary."""
        return cls(
            data_source=DataSource.from_dict(data["data_source"]) if data["data_source"] else None,
            transforms=[Transform.from_dict(t) for t in data["transforms"]],
            chart_config=ChartConfig.from_dict(data["chart_config"]),
            theme=Theme.from_dict(data["theme"]),
        )


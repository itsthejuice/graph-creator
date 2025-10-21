"""Chart rendering engines."""

from .mpl_renderer import MatplotlibRenderer

__all__ = ["MatplotlibRenderer"]

# Optional Plotly support
try:
    from .plotly_renderer import PlotlyRenderer
    __all__.append("PlotlyRenderer")
except ImportError:
    PlotlyRenderer = None


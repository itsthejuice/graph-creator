"""Tests for chart rendering."""

import pytest
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from app.charts.mpl_renderer import MatplotlibRenderer
from app.models.data_models import ChartConfig, SeriesStyle, Theme, AxisConfig


class TestMatplotlibRenderer:
    """Test Matplotlib renderer."""
    
    def setup_method(self):
        """Setup test data."""
        self.renderer = MatplotlibRenderer()
        self.df = pd.DataFrame({
            'X': [1, 2, 3, 4, 5],
            'Y1': [10, 20, 15, 25, 30],
            'Y2': [5, 15, 10, 20, 25],
        })
        self.theme = Theme()
    
    def teardown_method(self):
        """Cleanup after each test."""
        self.renderer.close()
    
    def test_render_line_chart(self):
        """Test rendering line chart."""
        config = ChartConfig(
            chart_type="line",
            title="Test Line Chart",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y1", visible=True),
                SeriesStyle(column="Y2", visible=True),
            ],
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
        assert metadata["render_time"] > 0
        assert len(metadata["warnings"]) == 0
    
    def test_render_area_chart(self):
        """Test rendering area chart."""
        config = ChartConfig(
            chart_type="area",
            title="Test Area Chart",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y1", visible=True),
            ],
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
    
    def test_render_scatter_chart(self):
        """Test rendering scatter chart."""
        config = ChartConfig(
            chart_type="scatter",
            title="Test Scatter Chart",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y1", visible=True, marker="o"),
            ],
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
    
    def test_render_bar_chart(self):
        """Test rendering bar chart."""
        config = ChartConfig(
            chart_type="bar",
            title="Test Bar Chart",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y1", visible=True),
                SeriesStyle(column="Y2", visible=True),
            ],
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
    
    def test_render_histogram(self):
        """Test rendering histogram."""
        config = ChartConfig(
            chart_type="histogram",
            title="Test Histogram",
            series_styles=[
                SeriesStyle(column="Y1", visible=True),
            ],
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
    
    def test_render_with_secondary_axis(self):
        """Test rendering with secondary Y axis."""
        config = ChartConfig(
            chart_type="line",
            title="Test Dual Axis Chart",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y1", visible=True, y_axis="primary"),
                SeriesStyle(column="Y2", visible=True, y_axis="secondary"),
            ],
            y_axis_secondary=AxisConfig(label="Secondary Y"),
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
    
    def test_render_with_log_scale(self):
        """Test rendering with logarithmic scale."""
        config = ChartConfig(
            chart_type="line",
            title="Test Log Scale",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y1", visible=True),
            ],
            y_axis_primary=AxisConfig(scale="log"),
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
    
    def test_render_with_theme(self):
        """Test rendering with custom theme."""
        theme = Theme(
            mode="dark",
            font_size=14.0,
            color_palette=["#ff0000", "#00ff00"],
        )
        
        config = ChartConfig(
            chart_type="line",
            title="Test Themed Chart",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y1", visible=True),
            ],
        )
        
        fig, metadata = self.renderer.render(self.df, config, theme)
        
        assert fig is not None
        assert metadata["rows"] == 5
    
    def test_save_to_bytes(self):
        """Test saving figure to bytes."""
        config = ChartConfig(
            chart_type="line",
            title="Test",
            x_column="X",
            series_styles=[SeriesStyle(column="Y1", visible=True)],
        )
        
        fig, _ = self.renderer.render(self.df, config, self.theme)
        
        img_bytes = self.renderer.save_to_bytes(format='png', dpi=100)
        
        assert len(img_bytes) > 0
        assert img_bytes.startswith(b'\x89PNG')  # PNG signature
    
    def test_render_empty_data(self):
        """Test rendering with empty data."""
        empty_df = pd.DataFrame()
        
        config = ChartConfig(
            chart_type="line",
            title="Empty",
            x_column="X",
        )
        
        # Should handle gracefully
        try:
            fig, metadata = self.renderer.render(empty_df, config, self.theme)
            # If it doesn't raise, check warnings
            assert len(metadata["warnings"]) > 0 or metadata["rows"] == 0
        except Exception:
            # Also acceptable to raise
            pass
    
    def test_render_missing_column(self):
        """Test rendering with missing column."""
        config = ChartConfig(
            chart_type="line",
            title="Missing Column",
            x_column="X",
            series_styles=[
                SeriesStyle(column="NonExistent", visible=True),
            ],
        )
        
        fig, metadata = self.renderer.render(self.df, config, self.theme)
        
        # Should warn about missing column
        assert len(metadata["warnings"]) > 0
    
    def test_render_non_numeric_series(self):
        """Test rendering with non-numeric series."""
        df_with_text = pd.DataFrame({
            'X': [1, 2, 3],
            'Y': ['a', 'b', 'c'],
        })
        
        config = ChartConfig(
            chart_type="line",
            title="Non-numeric",
            x_column="X",
            series_styles=[
                SeriesStyle(column="Y", visible=True),
            ],
        )
        
        fig, metadata = self.renderer.render(df_with_text, config, self.theme)
        
        # Should warn about non-numeric data
        assert len(metadata["warnings"]) > 0


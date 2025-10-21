"""Tests for serialization and project I/O."""

import pytest
import tempfile
import json
from pathlib import Path
import pandas as pd

from app.models.data_models import (
    DataSource,
    ChartConfig,
    SeriesStyle,
    Theme,
    ProjectState,
)
from app.services.project_io import ProjectIO


class TestSerialization:
    """Test serialization of data models."""
    
    def test_data_source_serialization(self):
        """Test DataSource to/from dict."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
        })
        
        ds = DataSource(name="Test", df=df, source_type="csv")
        
        # Serialize
        data = ds.to_dict()
        
        # Deserialize
        ds2 = DataSource.from_dict(data)
        
        assert ds2.name == ds.name
        assert ds2.source_type == ds.source_type
        assert ds2.df.equals(ds.df)
    
    def test_series_style_serialization(self):
        """Test SeriesStyle to/from dict."""
        style = SeriesStyle(
            column="A",
            visible=True,
            line_width=2.5,
            color="#ff0000",
            alpha=0.8,
        )
        
        # Serialize
        data = style.to_dict()
        
        # Deserialize
        style2 = SeriesStyle.from_dict(data)
        
        assert style2.column == style.column
        assert style2.visible == style.visible
        assert style2.line_width == style.line_width
        assert style2.color == style.color
        assert style2.alpha == style.alpha
    
    def test_chart_config_serialization(self):
        """Test ChartConfig to/from dict."""
        config = ChartConfig(
            chart_type="line",
            title="Test Chart",
            x_column="X",
            series_styles=[
                SeriesStyle(column="A"),
                SeriesStyle(column="B"),
            ],
        )
        
        # Serialize
        data = config.to_dict()
        
        # Deserialize
        config2 = ChartConfig.from_dict(data)
        
        assert config2.chart_type == config.chart_type
        assert config2.title == config.title
        assert config2.x_column == config.x_column
        assert len(config2.series_styles) == len(config.series_styles)
    
    def test_theme_serialization(self):
        """Test Theme to/from dict."""
        theme = Theme(
            name="custom",
            mode="dark",
            font_size=12.0,
            color_palette=["#ff0000", "#00ff00", "#0000ff"],
        )
        
        # Serialize
        data = theme.to_dict()
        
        # Deserialize
        theme2 = Theme.from_dict(data)
        
        assert theme2.name == theme.name
        assert theme2.mode == theme.mode
        assert theme2.font_size == theme.font_size
        assert theme2.color_palette == theme.color_palette
    
    def test_project_state_serialization(self):
        """Test ProjectState to/from dict."""
        df = pd.DataFrame({'A': [1, 2, 3]})
        
        project = ProjectState(
            data_source=DataSource(name="Test", df=df),
            chart_config=ChartConfig(title="Test"),
            theme=Theme(name="test"),
        )
        
        # Serialize
        data = project.to_dict()
        
        # Deserialize
        project2 = ProjectState.from_dict(data)
        
        assert project2.data_source.name == project.data_source.name
        assert project2.chart_config.title == project.chart_config.title
        assert project2.theme.name == project.theme.name


class TestProjectIO:
    """Test project file I/O."""
    
    def test_save_and_load_project(self):
        """Test saving and loading project files."""
        df = pd.DataFrame({
            'X': [1, 2, 3],
            'Y': [4, 5, 6],
        })
        
        project = ProjectState(
            data_source=DataSource(name="Test Data", df=df),
            chart_config=ChartConfig(
                chart_type="line",
                title="Test Chart",
                x_column="X",
                series_styles=[SeriesStyle(column="Y")],
            ),
            theme=Theme(mode="light"),
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.graphproj', delete=False) as f:
            temp_path = f.name
        
        try:
            ProjectIO.save_project(project, temp_path)
            
            # Verify file exists and is valid JSON
            assert Path(temp_path).exists()
            
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            assert "data_source" in data
            assert "chart_config" in data
            assert "theme" in data
            
            # Load project
            loaded_project = ProjectIO.load_project(temp_path)
            
            assert loaded_project.data_source.name == project.data_source.name
            assert loaded_project.chart_config.title == project.chart_config.title
            assert loaded_project.theme.mode == project.theme.mode
        
        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)
    
    def test_export_data_csv(self):
        """Test exporting data to CSV."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            ProjectIO.export_data_csv(temp_path, df)
            
            # Load and verify
            loaded_df = pd.read_csv(temp_path)
            assert loaded_df.equals(df)
        
        finally:
            Path(temp_path).unlink(missing_ok=True)
    
    def test_export_data_json(self):
        """Test exporting data to JSON."""
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
        })
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            ProjectIO.export_data_json(temp_path, df)
            
            # Verify file exists and is valid JSON
            assert Path(temp_path).exists()
            
            with open(temp_path, 'r') as f:
                data = json.load(f)
            
            assert isinstance(data, list)
            assert len(data) == 3
        
        finally:
            Path(temp_path).unlink(missing_ok=True)


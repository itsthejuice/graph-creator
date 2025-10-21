"""Tests for transform engine."""

import pytest
import pandas as pd
import numpy as np

from app.services.transforms import TransformEngine
from app.models.data_models import Transform


class TestTransformEngine:
    """Test transform engine functionality."""
    
    def setup_method(self):
        """Setup test data."""
        self.engine = TransformEngine()
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [10, 20, 30, 40, 50],
            'C': [100, 200, 300, 400, 500],
        })
    
    def test_column_math_add(self):
        """Test column addition."""
        transform = Transform(
            transform_type="column_math",
            params={
                "operation": "add",
                "columns": ["A", "B"],
                "new_column": "sum",
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        assert "sum" in result.columns
        assert result["sum"].tolist() == [11, 22, 33, 44, 55]
    
    def test_column_math_subtract(self):
        """Test column subtraction."""
        transform = Transform(
            transform_type="column_math",
            params={
                "operation": "subtract",
                "columns": ["B", "A"],
                "new_column": "diff",
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        assert "diff" in result.columns
        assert result["diff"].tolist() == [9, 18, 27, 36, 45]
    
    def test_normalize_minmax(self):
        """Test min-max normalization."""
        transform = Transform(
            transform_type="normalize",
            params={
                "method": "min-max",
                "columns": ["A"],
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        assert result["A"].min() == 0.0
        assert result["A"].max() == 1.0
    
    def test_normalize_zscore(self):
        """Test z-score normalization."""
        transform = Transform(
            transform_type="normalize",
            params={
                "method": "z-score",
                "columns": ["A"],
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        # Z-score should have mean ~0 and std ~1
        assert abs(result["A"].mean()) < 0.01
        # Note: std will be slightly different due to sample vs population
    
    def test_rolling_mean(self):
        """Test rolling mean."""
        transform = Transform(
            transform_type="rolling",
            params={
                "window": 3,
                "operation": "mean",
                "columns": ["A"],
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        # Middle values should be averages
        assert result["A"].iloc[2] == 2.0  # (1+2+3)/3
    
    def test_diff(self):
        """Test difference calculation."""
        transform = Transform(
            transform_type="diff",
            params={
                "periods": 1,
                "columns": ["A"],
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        # First value is NaN, rest are 1
        assert pd.isna(result["A"].iloc[0])
        assert all(result["A"].iloc[1:] == 1)
    
    def test_pct_change(self):
        """Test percentage change."""
        transform = Transform(
            transform_type="pct_change",
            params={
                "periods": 1,
                "columns": ["B"],
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        # First value is NaN, rest are 100% increase
        assert pd.isna(result["B"].iloc[0])
        assert all(abs(result["B"].iloc[1:] - 100.0) < 0.01)
    
    def test_filter(self):
        """Test row filtering."""
        transform = Transform(
            transform_type="filter",
            params={
                "query": "A > 2",
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        assert len(result) == 3
        assert result["A"].tolist() == [3, 4, 5]
    
    def test_computed_series(self):
        """Test computed series."""
        transform = Transform(
            transform_type="computed_series",
            params={
                "expression": "A * 2 + B",
                "new_column": "computed",
            },
        )
        
        result = self.engine.apply_transform(self.df, transform)
        
        assert "computed" in result.columns
        assert result["computed"].tolist() == [12, 24, 36, 48, 60]
    
    def test_interpolate(self):
        """Test interpolation."""
        df_with_nan = pd.DataFrame({
            'A': [1.0, np.nan, 3.0, np.nan, 5.0],
        })
        
        transform = Transform(
            transform_type="interpolate",
            params={
                "method": "linear",
                "columns": ["A"],
            },
        )
        
        result = self.engine.apply_transform(df_with_nan, transform)
        
        # NaN values should be interpolated
        assert not result["A"].isna().any()
        assert result["A"].iloc[1] == 2.0
        assert result["A"].iloc[3] == 4.0


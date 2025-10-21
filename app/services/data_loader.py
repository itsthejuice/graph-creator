"""Data loading utilities."""

import io
from typing import Optional
import pandas as pd
import numpy as np
from datetime import datetime

from ..models.data_models import DataSource


class DataLoader:
    """Handles loading data from various sources."""
    
    @staticmethod
    def from_csv(content: str, name: str = "Data") -> DataSource:
        """Load data from CSV content."""
        df = pd.read_csv(io.StringIO(content))
        return DataSource(
            name=name,
            df=df,
            source_type="csv",
            created_at=datetime.now(),
        )
    
    @staticmethod
    def from_tsv(content: str, name: str = "Data") -> DataSource:
        """Load data from TSV content."""
        df = pd.read_csv(io.StringIO(content), sep='\t')
        return DataSource(
            name=name,
            df=df,
            source_type="csv",
            created_at=datetime.now(),
        )
    
    @staticmethod
    def from_json(content: str, name: str = "Data") -> DataSource:
        """Load data from JSON content."""
        df = pd.read_json(io.StringIO(content))
        return DataSource(
            name=name,
            df=df,
            source_type="json",
            created_at=datetime.now(),
        )
    
    @staticmethod
    def from_clipboard(content: str, name: str = "Data") -> DataSource:
        """Load data from clipboard content."""
        # Try to detect separator
        lines = content.strip().split('\n')
        if not lines:
            raise ValueError("Empty clipboard content")
        
        # Try tab first, then comma
        first_line = lines[0]
        if '\t' in first_line:
            df = pd.read_csv(io.StringIO(content), sep='\t')
        else:
            df = pd.read_csv(io.StringIO(content))
        
        return DataSource(
            name=name,
            df=df,
            source_type="clipboard",
            created_at=datetime.now(),
        )
    
    @staticmethod
    def from_dataframe(df: pd.DataFrame, name: str = "Data") -> DataSource:
        """Create DataSource from existing DataFrame."""
        return DataSource(
            name=name,
            df=df.copy(),
            source_type="manual",
            created_at=datetime.now(),
        )
    
    @staticmethod
    def infer_column_types(df: pd.DataFrame) -> pd.DataFrame:
        """Infer and convert column types."""
        result = df.copy()
        
        for col in result.columns:
            # Try datetime
            try:
                converted = pd.to_datetime(result[col], errors='coerce')
                if converted.notna().sum() > len(result) * 0.8:  # 80% success
                    result[col] = converted
                    continue
            except Exception:
                pass
            
            # Try numeric
            try:
                converted = pd.to_numeric(result[col], errors='coerce')
                if converted.notna().sum() > len(result) * 0.8:  # 80% success
                    result[col] = converted
                    continue
            except Exception:
                pass
        
        return result
    
    @staticmethod
    def create_example_overlapping_trends() -> DataSource:
        """Create example data for overlapping trends."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        
        df = pd.DataFrame({
            'Date': dates,
            'Metric A': 100 + pd.Series(range(100)) * 0.5 + pd.Series(range(100)).apply(lambda x: 10 * np.sin(x / 10)),
            'Metric B': 80 + pd.Series(range(100)) * 0.3 + pd.Series(range(100)).apply(lambda x: 8 * np.cos(x / 15)),
            'Metric C': 120 + pd.Series(range(100)) * 0.2 + pd.Series(range(100)).apply(lambda x: 5 * np.sin(x / 8)),
        })
        
        return DataSource(
            name="Overlapping Trends Example",
            df=df,
            source_type="manual",
        )
    
    @staticmethod
    def create_example_economic() -> DataSource:
        """Create example economic data with dual axes."""
        dates = pd.date_range('2020-01-01', periods=48, freq='M')
        
        df = pd.DataFrame({
            'Date': dates,
            'GDP (Billions)': 20000 + pd.Series(range(48)) * 100 + pd.Series(range(48)).apply(lambda x: 500 * np.sin(x / 6)),
            'Unemployment (%)': 5 + pd.Series(range(48)).apply(lambda x: 2 * np.sin(x / 8 + 1)),
            'Interest Rate (%)': 2 + pd.Series(range(48)).apply(lambda x: 1.5 * np.cos(x / 10)),
        })
        
        return DataSource(
            name="Economic Indicators Example",
            df=df,
            source_type="manual",
        )
    
    @staticmethod
    def create_example_contamination() -> DataSource:
        """Create example contamination vs rawness data."""
        samples = list(range(1, 31))
        
        df = pd.DataFrame({
            'Sample': samples,
            'Contamination (ppm)': [2, 3, 2.5, 4, 5, 3, 2, 1, 1.5, 2, 3.5, 5, 6, 7, 5, 4, 3, 2.5, 2, 1.5, 
                                    1, 2, 3, 4, 5, 6, 5.5, 4.5, 3.5, 2.5],
            'Rawness Index': [95, 93, 94, 90, 85, 92, 96, 98, 97, 95, 91, 86, 80, 75, 84, 88, 92, 93, 95, 96,
                             98, 96, 93, 89, 86, 82, 84, 87, 91, 94],
        })
        
        return DataSource(
            name="Contamination vs Rawness Example",
            df=df,
            source_type="manual",
        )
    
    @staticmethod
    def create_blank_data() -> DataSource:
        """Create blank/minimal data for new graphs."""
        df = pd.DataFrame({
            'X': [0],
            'Y': [0],
        })
        
        return DataSource(
            name="Blank",
            df=df,
            source_type="manual",
        )


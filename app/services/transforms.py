"""Data transformation engine."""

from typing import Any, Dict
import pandas as pd
import numpy as np
from scipy import stats


class TransformEngine:
    """Engine for applying data transformations."""
    
    def apply_transform(self, df: pd.DataFrame, transform: Any) -> pd.DataFrame:
        """Apply a transform to a dataframe."""
        transform_type = transform.transform_type
        params = transform.params
        
        method_map = {
            "column_math": self._column_math,
            "normalize": self._normalize,
            "smooth": self._smooth,
            "resample": self._resample,
            "interpolate": self._interpolate,
            "filter": self._filter,
            "group": self._group,
            "computed_series": self._computed_series,
            "rolling": self._rolling,
            "diff": self._diff,
            "pct_change": self._pct_change,
        }
        
        method = method_map.get(transform_type)
        if method is None:
            raise ValueError(f"Unknown transform type: {transform_type}")
        
        return method(df, params)
    
    def _column_math(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Perform column math operations."""
        result = df.copy()
        operation = params.get("operation", "add")
        columns = params.get("columns", [])
        new_column = params.get("new_column", "result")
        
        if len(columns) < 2:
            return result
        
        if operation == "add":
            result[new_column] = sum(df[col] for col in columns if col in df.columns)
        elif operation == "subtract":
            result[new_column] = df[columns[0]]
            for col in columns[1:]:
                if col in df.columns:
                    result[new_column] -= df[col]
        elif operation == "multiply":
            result[new_column] = df[columns[0]]
            for col in columns[1:]:
                if col in df.columns:
                    result[new_column] *= df[col]
        elif operation == "divide":
            result[new_column] = df[columns[0]]
            for col in columns[1:]:
                if col in df.columns:
                    result[new_column] /= df[col]
        
        return result
    
    def _normalize(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Normalize columns."""
        result = df.copy()
        method = params.get("method", "min-max")
        columns = params.get("columns", [])
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            if method == "min-max":
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val > min_val:
                    result[col] = (df[col] - min_val) / (max_val - min_val)
            elif method == "z-score":
                result[col] = stats.zscore(df[col].dropna())
            elif method == "robust":
                median = df[col].median()
                iqr = df[col].quantile(0.75) - df[col].quantile(0.25)
                if iqr > 0:
                    result[col] = (df[col] - median) / iqr
        
        return result
    
    def _smooth(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Apply smoothing to columns."""
        result = df.copy()
        method = params.get("method", "rolling_mean")
        window = params.get("window", 3)
        columns = params.get("columns", [])
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            if method == "rolling_mean":
                result[col] = df[col].rolling(window=window, center=True).mean()
            elif method == "rolling_median":
                result[col] = df[col].rolling(window=window, center=True).median()
            elif method == "ewm":
                result[col] = df[col].ewm(span=window).mean()
        
        return result
    
    def _resample(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Resample time series data."""
        freq = params.get("freq", "D")
        agg = params.get("agg", "mean")
        date_column = params.get("date_column")
        
        if date_column not in df.columns:
            return df
        
        result = df.copy()
        result[date_column] = pd.to_datetime(result[date_column])
        result = result.set_index(date_column)
        
        if agg == "mean":
            result = result.resample(freq).mean()
        elif agg == "sum":
            result = result.resample(freq).sum()
        elif agg == "first":
            result = result.resample(freq).first()
        elif agg == "last":
            result = result.resample(freq).last()
        
        return result.reset_index()
    
    def _interpolate(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Interpolate missing values."""
        result = df.copy()
        method = params.get("method", "linear")
        columns = params.get("columns", [])
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if pd.api.types.is_numeric_dtype(df[col]):
                result[col] = df[col].interpolate(method=method)
        
        return result
    
    def _filter(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Filter rows by query."""
        query = params.get("query", "")
        
        if not query:
            return df
        
        try:
            return df.query(query)
        except Exception:
            return df
    
    def _group(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Group and aggregate data."""
        group_by = params.get("group_by", [])
        agg_func = params.get("agg_func", "mean")
        
        if not group_by:
            return df
        
        # Filter valid group columns
        group_by = [col for col in group_by if col in df.columns]
        
        if not group_by:
            return df
        
        # Get numeric columns for aggregation
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in group_by]
        
        if not numeric_cols:
            return df
        
        if agg_func == "mean":
            result = df.groupby(group_by)[numeric_cols].mean().reset_index()
        elif agg_func == "sum":
            result = df.groupby(group_by)[numeric_cols].sum().reset_index()
        elif agg_func == "count":
            result = df.groupby(group_by)[numeric_cols].count().reset_index()
        elif agg_func == "min":
            result = df.groupby(group_by)[numeric_cols].min().reset_index()
        elif agg_func == "max":
            result = df.groupby(group_by)[numeric_cols].max().reset_index()
        else:
            result = df
        
        return result
    
    def _computed_series(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Create computed series using expression."""
        result = df.copy()
        expression = params.get("expression", "")
        new_column = params.get("new_column", "computed")
        
        if not expression:
            return result
        
        try:
            # Create safe namespace for eval
            namespace = {
                "df": df,
                "np": np,
                "pd": pd,
            }
            
            # Add columns to namespace
            for col in df.columns:
                namespace[col] = df[col]
            
            # Evaluate expression
            result[new_column] = eval(expression, {"__builtins__": {}}, namespace)
        except Exception as e:
            print(f"Expression error: {e}")
        
        return result
    
    def _rolling(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Apply rolling window operations."""
        result = df.copy()
        window = params.get("window", 3)
        operation = params.get("operation", "mean")
        columns = params.get("columns", [])
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if not pd.api.types.is_numeric_dtype(df[col]):
                continue
            
            rolling = df[col].rolling(window=window)
            
            if operation == "mean":
                result[col] = rolling.mean()
            elif operation == "median":
                result[col] = rolling.median()
            elif operation == "sum":
                result[col] = rolling.sum()
            elif operation == "std":
                result[col] = rolling.std()
            elif operation == "min":
                result[col] = rolling.min()
            elif operation == "max":
                result[col] = rolling.max()
        
        return result
    
    def _diff(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Calculate difference between consecutive rows."""
        result = df.copy()
        periods = params.get("periods", 1)
        columns = params.get("columns", [])
        
        for col in columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                result[col] = df[col].diff(periods=periods)
        
        return result
    
    def _pct_change(self, df: pd.DataFrame, params: Dict[str, Any]) -> pd.DataFrame:
        """Calculate percentage change between consecutive rows."""
        result = df.copy()
        periods = params.get("periods", 1)
        columns = params.get("columns", [])
        
        for col in columns:
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                result[col] = df[col].pct_change(periods=periods) * 100
        
        return result


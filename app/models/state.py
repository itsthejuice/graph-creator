"""Application state management with undo/redo support."""

from typing import List, Optional, Callable
from dataclasses import dataclass, field
import copy
import pandas as pd

from .data_models import (
    DataSource,
    ChartConfig,
    Theme,
    Transform,
    ProjectState,
)


@dataclass
class AppState:
    """Main application state with undo/redo support."""
    
    # Current state
    data_source: Optional[DataSource] = None
    transforms: List[Transform] = field(default_factory=list)
    chart_config: ChartConfig = field(default_factory=ChartConfig)
    theme: Theme = field(default_factory=Theme)
    
    # UI state
    use_interactive_preview: bool = False
    show_grid: bool = True
    auto_render: bool = True
    
    # History for undo/redo
    _history: List[ProjectState] = field(default_factory=list, init=False, repr=False)
    _history_index: int = field(default=-1, init=False, repr=False)
    _max_history: int = field(default=50, init=False, repr=False)
    
    # Change listeners
    _listeners: List[Callable] = field(default_factory=list, init=False, repr=False)
    
    def add_listener(self, listener: Callable) -> None:
        """Add a change listener."""
        self._listeners.append(listener)
    
    def remove_listener(self, listener: Callable) -> None:
        """Remove a change listener."""
        if listener in self._listeners:
            self._listeners.remove(listener)
    
    def _notify_listeners(self) -> None:
        """Notify all listeners of state change."""
        for listener in self._listeners:
            try:
                listener()
            except Exception as e:
                print(f"Error in listener: {e}")
    
    def save_snapshot(self) -> None:
        """Save current state to history."""
        # Remove any history after current index
        self._history = self._history[:self._history_index + 1]
        
        # Create snapshot
        snapshot = ProjectState(
            data_source=copy.deepcopy(self.data_source),
            transforms=copy.deepcopy(self.transforms),
            chart_config=copy.deepcopy(self.chart_config),
            theme=copy.deepcopy(self.theme),
        )
        
        # Add to history
        self._history.append(snapshot)
        
        # Limit history size
        if len(self._history) > self._max_history:
            self._history.pop(0)
        else:
            self._history_index += 1
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return self._history_index > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return self._history_index < len(self._history) - 1
    
    def undo(self) -> bool:
        """Undo last change."""
        if not self.can_undo():
            return False
        
        self._history_index -= 1
        self._restore_from_history()
        self._notify_listeners()
        return True
    
    def redo(self) -> bool:
        """Redo last undone change."""
        if not self.can_redo():
            return False
        
        self._history_index += 1
        self._restore_from_history()
        self._notify_listeners()
        return True
    
    def _restore_from_history(self) -> None:
        """Restore state from history at current index."""
        if 0 <= self._history_index < len(self._history):
            snapshot = self._history[self._history_index]
            self.data_source = copy.deepcopy(snapshot.data_source)
            self.transforms = copy.deepcopy(snapshot.transforms)
            self.chart_config = copy.deepcopy(snapshot.chart_config)
            self.theme = copy.deepcopy(snapshot.theme)
    
    def get_transformed_data(self) -> Optional[pd.DataFrame]:
        """Get data after applying all enabled transforms."""
        if self.data_source is None:
            return None
        
        df = self.data_source.df.copy()
        
        # Import here to avoid circular dependency
        from ..services.transforms import TransformEngine
        engine = TransformEngine()
        
        for transform in self.transforms:
            if transform.enabled:
                try:
                    df = engine.apply_transform(df, transform)
                except Exception as e:
                    print(f"Transform error: {e}")
        
        return df
    
    def load_project_state(self, project: ProjectState) -> None:
        """Load a complete project state."""
        self.data_source = copy.deepcopy(project.data_source)
        self.transforms = copy.deepcopy(project.transforms)
        self.chart_config = copy.deepcopy(project.chart_config)
        self.theme = copy.deepcopy(project.theme)
        
        # Reset history
        self._history.clear()
        self._history_index = -1
        self.save_snapshot()
        
        self._notify_listeners()
    
    def get_project_state(self) -> ProjectState:
        """Get current project state for saving."""
        return ProjectState(
            data_source=copy.deepcopy(self.data_source),
            transforms=copy.deepcopy(self.transforms),
            chart_config=copy.deepcopy(self.chart_config),
            theme=copy.deepcopy(self.theme),
        )
    
    def reset_to_defaults(self) -> None:
        """Reset to default state."""
        self.data_source = None
        self.transforms.clear()
        self.chart_config = ChartConfig()
        self.theme = Theme()
        self._history.clear()
        self._history_index = -1
        self.save_snapshot()
        self._notify_listeners()


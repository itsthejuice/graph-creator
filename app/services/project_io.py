"""Project save/load functionality."""

import json
from pathlib import Path
from typing import Optional

from ..models.data_models import ProjectState


class ProjectIO:
    """Handles project file I/O."""
    
    @staticmethod
    def save_project(project: ProjectState, file_path: str) -> None:
        """Save project to .graphproj file."""
        data = project.to_dict()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
    
    @staticmethod
    def load_project(file_path: str) -> ProjectState:
        """Load project from .graphproj file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return ProjectState.from_dict(data)
    
    @staticmethod
    def export_data_csv(file_path: str, df) -> None:
        """Export DataFrame to CSV."""
        if df is not None:
            df.to_csv(file_path, index=False)
    
    @staticmethod
    def export_data_json(file_path: str, df) -> None:
        """Export DataFrame to JSON."""
        if df is not None:
            df.to_json(file_path, orient='records', indent=2)


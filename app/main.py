"""Main application entry point."""

import flet as ft
import logging
import sys
from pathlib import Path

from .models.state import AppState
from .models.data_models import ChartConfig, SeriesStyle
from .services.data_loader import DataLoader
from .services.project_io import ProjectIO
from .ui.builder import Builder
from .ui.canvas import Canvas
from .ui.dialogs import FilePickerDialog, TextInputDialog, ErrorDialog, SuccessDialog

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class GraphCreatorApp:
    """Main application class."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.state = AppState()
        self.file_picker = FilePickerDialog(page)
        
        # Configure page
        page.title = "Graph Creator"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 0
        
        # Setup keyboard shortcuts
        page.on_keyboard_event = self._handle_keyboard
        
        # Build UI
        self._build_ui()
        
        # Load default example
        self._load_example("overlapping")
        
        # Add state listener
        self.state.add_listener(self._on_state_change)
    
    def _build_ui(self):
        """Build the main UI."""
        # Create builder and canvas
        self.builder = Builder(
            state=self.state,
            on_change=self._on_config_change,
            on_load_example=self._load_example,
            on_import_data=self._import_data,
        )
        
        self.canvas = Canvas(
            state=self.state,
            on_export=self._export,
        )
        
        # Create layout
        content = ft.Row([
            self.builder,
            ft.VerticalDivider(width=1),
            self.canvas,
        ], spacing=0, expand=True)
        
        self.page.add(content)
    
    def _handle_keyboard(self, e: ft.KeyboardEvent):
        """Handle keyboard shortcuts."""
        if e.ctrl:
            if e.key == "S":
                # Save project
                self._save_project()
            elif e.key == "E":
                # Export image
                self._export("png")
            elif e.key == "Z":
                # Undo
                if self.state.can_undo():
                    self.state.undo()
                    self._refresh_ui()
            elif e.key == "Y":
                # Redo
                if self.state.can_redo():
                    self.state.redo()
                    self._refresh_ui()
            elif e.key == "N":
                # New project
                self._new_project()
    
    def _on_state_change(self):
        """Handle state change."""
        self._refresh_ui()
    
    def _on_config_change(self):
        """Handle configuration change."""
        self.state.save_snapshot()
        if self.state.auto_render:
            self.canvas.render()
        self.builder.refresh()
    
    def _refresh_ui(self):
        """Refresh entire UI."""
        self.canvas.render()
        self.builder.refresh()
        self.page.update()
    
    def _load_example(self, example_type: str):
        """Load an example dataset."""
        try:
            if example_type == "overlapping":
                data_source = DataLoader.create_example_overlapping_trends()
                # Configure chart for overlapping lines
                self.state.data_source = data_source
                self.state.chart_config = ChartConfig(
                    chart_type="line",
                    title="Overlapping Multi-Series Trends",
                    subtitle="Example of multiple overlapping line series",
                    x_column="Date",
                )
                # Auto-create series
                self._auto_create_series()
                
            elif example_type == "economic":
                data_source = DataLoader.create_example_economic()
                self.state.data_source = data_source
                self.state.chart_config = ChartConfig(
                    chart_type="line",
                    title="Economic Indicators",
                    subtitle="Multi-axis economic data",
                    x_column="Date",
                )
                self._auto_create_series()
                
            elif example_type == "contamination":
                data_source = DataLoader.create_example_contamination()
                self.state.data_source = data_source
                self.state.chart_config = ChartConfig(
                    chart_type="line",
                    title="Contamination vs Rawness",
                    subtitle="Relationship between contamination and rawness index",
                    x_column="Sample",
                )
                self._auto_create_series()
            
            self.state.save_snapshot()
            self._refresh_ui()
            
            self._show_success("Example Loaded", f"Loaded {example_type} example successfully")
        
        except Exception as e:
            logger.error(f"Error loading example: {e}")
            self._show_error("Error", f"Failed to load example: {str(e)}")
    
    def _auto_create_series(self):
        """Auto-create series styles for numeric columns."""
        df = self.state.get_transformed_data()
        if df is None:
            return
        
        # Get numeric columns (excluding X column)
        x_col = self.state.chart_config.x_column
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if x_col in numeric_cols:
            numeric_cols.remove(x_col)
        
        # Clear existing series
        self.state.chart_config.series_styles.clear()
        
        # Create series styles
        for col in numeric_cols[:10]:  # Limit to 10 series
            self.state.chart_config.series_styles.append(
                SeriesStyle(column=col, visible=True)
            )
    
    def _import_data(self, source_type: str):
        """Import data from various sources."""
        if source_type == "csv":
            self.file_picker.pick_file(
                allowed_extensions=["csv"],
                on_result=self._on_csv_picked,
            )
        elif source_type == "json":
            self.file_picker.pick_file(
                allowed_extensions=["json"],
                on_result=self._on_json_picked,
            )
        elif source_type == "clipboard":
            self._show_clipboard_dialog()
        elif source_type == "project":
            self.file_picker.pick_file(
                allowed_extensions=["graphproj", "json"],
                on_result=self._on_project_picked,
            )
    
    def _on_csv_picked(self, e: ft.FilePickerResultEvent):
        """Handle CSV file picked."""
        if e.files:
            try:
                file_path = e.files[0].path
                with open(file_path, 'r') as f:
                    content = f.read()
                
                data_source = DataLoader.from_csv(content, name=Path(file_path).stem)
                data_source.df = DataLoader.infer_column_types(data_source.df)
                
                self.state.data_source = data_source
                self.state.chart_config.series_styles.clear()
                self._auto_create_series()
                self.state.save_snapshot()
                self._refresh_ui()
                
                self._show_success("Data Imported", f"Loaded {len(data_source.df)} rows")
            
            except Exception as e:
                logger.error(f"Error loading CSV: {e}")
                self._show_error("Import Error", str(e))
    
    def _on_json_picked(self, e: ft.FilePickerResultEvent):
        """Handle JSON file picked."""
        if e.files:
            try:
                file_path = e.files[0].path
                with open(file_path, 'r') as f:
                    content = f.read()
                
                data_source = DataLoader.from_json(content, name=Path(file_path).stem)
                data_source.df = DataLoader.infer_column_types(data_source.df)
                
                self.state.data_source = data_source
                self.state.chart_config.series_styles.clear()
                self._auto_create_series()
                self.state.save_snapshot()
                self._refresh_ui()
                
                self._show_success("Data Imported", f"Loaded {len(data_source.df)} rows")
            
            except Exception as e:
                logger.error(f"Error loading JSON: {e}")
                self._show_error("Import Error", str(e))
    
    def _show_clipboard_dialog(self):
        """Show clipboard paste dialog."""
        dialog = TextInputDialog(
            title="Paste Data from Clipboard",
            label="Paste your data (CSV/TSV format)",
            multiline=True,
            on_submit=self._on_clipboard_submit,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _on_clipboard_submit(self, content: str):
        """Handle clipboard data submission."""
        try:
            data_source = DataLoader.from_clipboard(content, name="Clipboard Data")
            data_source.df = DataLoader.infer_column_types(data_source.df)
            
            self.state.data_source = data_source
            self.state.chart_config.series_styles.clear()
            self._auto_create_series()
            self.state.save_snapshot()
            self._refresh_ui()
            
            self._show_success("Data Imported", f"Loaded {len(data_source.df)} rows")
        
        except Exception as e:
            logger.error(f"Error loading clipboard data: {e}")
            self._show_error("Import Error", str(e))
    
    def _save_project(self):
        """Save project to file."""
        self.file_picker.save_file(
            file_name="project.graphproj",
            on_result=self._on_project_save,
        )
    
    def _on_project_save(self, e: ft.FilePickerResultEvent):
        """Handle project save."""
        if e.path:
            try:
                project = self.state.get_project_state()
                ProjectIO.save_project(project, e.path)
                self._show_success("Project Saved", f"Saved to {e.path}")
            
            except Exception as e:
                logger.error(f"Error saving project: {e}")
                self._show_error("Save Error", str(e))
    
    def _on_project_picked(self, e: ft.FilePickerResultEvent):
        """Handle project file picked."""
        if e.files:
            try:
                file_path = e.files[0].path
                project = ProjectIO.load_project(file_path)
                self.state.load_project_state(project)
                self._refresh_ui()
                self._show_success("Project Loaded", f"Loaded from {file_path}")
            
            except Exception as e:
                logger.error(f"Error loading project: {e}")
                self._show_error("Load Error", str(e))
    
    def _export(self, format: str):
        """Export chart or data."""
        if format in ["png", "svg", "pdf"]:
            self._export_image(format)
        elif format == "csv":
            self._export_data()
    
    def _export_image(self, format: str):
        """Export chart as image."""
        self.file_picker.save_file(
            file_name=f"chart.{format}",
            on_result=lambda e: self._on_image_export(e, format),
        )
    
    def _on_image_export(self, e: ft.FilePickerResultEvent, format: str):
        """Handle image export."""
        if e.path:
            try:
                dpi = 300  # High quality
                success = self.canvas.export_image(e.path, format=format, dpi=dpi)
                
                if success:
                    self._show_success("Export Successful", f"Saved to {e.path}")
                else:
                    self._show_error("Export Error", "Failed to export image")
            
            except Exception as e:
                logger.error(f"Error exporting image: {e}")
                self._show_error("Export Error", str(e))
    
    def _export_data(self):
        """Export data as CSV."""
        self.file_picker.save_file(
            file_name="data.csv",
            on_result=self._on_data_export,
        )
    
    def _on_data_export(self, e: ft.FilePickerResultEvent):
        """Handle data export."""
        if e.path:
            try:
                df = self.state.get_transformed_data()
                ProjectIO.export_data_csv(e.path, df)
                self._show_success("Export Successful", f"Saved to {e.path}")
            
            except Exception as e:
                logger.error(f"Error exporting data: {e}")
                self._show_error("Export Error", str(e))
    
    def _new_project(self):
        """Create new project."""
        self.state.reset_to_defaults()
        self._refresh_ui()
    
    def _show_error(self, title: str, message: str):
        """Show error dialog."""
        dialog = ErrorDialog(title, message)
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _show_success(self, title: str, message: str):
        """Show success dialog."""
        # Use snack bar for less intrusive notification
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(f"{title}: {message}"),
            action="OK",
        )
        self.page.snack_bar.open = True
        self.page.update()


def main():
    """Main entry point."""
    # Disable Flet telemetry
    import os
    os.environ["FLET_TELEMETRY_DISABLED"] = "1"
    
    ft.app(target=GraphCreatorApp)


if __name__ == "__main__":
    main()


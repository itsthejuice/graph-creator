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
        self.is_dark_mode = True  # Dark mode by default
        
        # Configure page
        page.title = "Graph Creator"
        page.padding = 0
        
        # Setup custom themes
        self._setup_themes()
        
        # Setup keyboard shortcuts
        page.on_keyboard_event = self._handle_keyboard
        
        # Build UI
        self._build_ui()
        
        # Load default example
        self._load_example("overlapping")
        
        # Add state listener
        self.state.add_listener(self._on_state_change)
    
    def _setup_themes(self):
        """Setup custom dark and light themes."""
        # Dark theme colors
        dark_colors = {
            'primary': '#3A82F7',
            'on_primary': '#E8EEF3',
            'primary_container': '#122738',
            'on_primary_container': '#E8EEF3',
            'secondary': '#4E9FB9',
            'on_secondary': '#E8EEF3',
            'secondary_container': '#18324A',
            'on_secondary_container': '#E8EEF3',
            'background': '#0C1A26',
            'on_background': '#E8EEF3',
            'surface': '#122738',
            'on_surface': '#E8EEF3',
            'surface_variant': '#18324A',
            'on_surface_variant': '#A5B3C0',
            'outline': '#4E9FB9',
            'error': '#C05555',
            'on_error': '#E8EEF3',
        }
        
        # Light theme colors
        light_colors = {
            'primary': '#2F6BDB',
            'on_primary': '#FFFFFF',
            'primary_container': '#E4EBF0',
            'on_primary_container': '#1E2B36',
            'secondary': '#5FA7D3',
            'on_secondary': '#FFFFFF',
            'secondary_container': '#E4EBF0',
            'on_secondary_container': '#1E2B36',
            'background': '#F6F9FB',
            'on_background': '#1E2B36',
            'surface': '#E4EBF0',
            'on_surface': '#1E2B36',
            'surface_variant': '#FFFFFF',
            'on_surface_variant': '#4B5E70',
            'outline': '#5FA7D3',
            'error': '#B23C3C',
            'on_error': '#FFFFFF',
        }
        
        self.page.theme = ft.Theme(
            color_scheme_seed=dark_colors['primary'],
            color_scheme=ft.ColorScheme(
                primary=dark_colors['primary'],
                on_primary=dark_colors['on_primary'],
                primary_container=dark_colors['primary_container'],
                on_primary_container=dark_colors['on_primary_container'],
                secondary=dark_colors['secondary'],
                on_secondary=dark_colors['on_secondary'],
                secondary_container=dark_colors['secondary_container'],
                on_secondary_container=dark_colors['on_secondary_container'],
                background=dark_colors['background'],
                on_background=dark_colors['on_background'],
                surface=dark_colors['surface'],
                on_surface=dark_colors['on_surface'],
                surface_variant=dark_colors['surface_variant'],
                on_surface_variant=dark_colors['on_surface_variant'],
                outline=dark_colors['outline'],
                error=dark_colors['error'],
                on_error=dark_colors['on_error'],
            ),
        )
        
        self.page.dark_theme = ft.Theme(
            color_scheme_seed=dark_colors['primary'],
            color_scheme=ft.ColorScheme(
                primary=dark_colors['primary'],
                on_primary=dark_colors['on_primary'],
                primary_container=dark_colors['primary_container'],
                on_primary_container=dark_colors['on_primary_container'],
                secondary=dark_colors['secondary'],
                on_secondary=dark_colors['on_secondary'],
                secondary_container=dark_colors['secondary_container'],
                on_secondary_container=dark_colors['on_secondary_container'],
                background=dark_colors['background'],
                on_background=dark_colors['on_background'],
                surface=dark_colors['surface'],
                on_surface=dark_colors['on_surface'],
                surface_variant=dark_colors['surface_variant'],
                on_surface_variant=dark_colors['on_surface_variant'],
                outline=dark_colors['outline'],
                error=dark_colors['error'],
                on_error=dark_colors['on_error'],
            ),
        )
        
        # Light theme (for when user toggles)
        self.light_theme = ft.Theme(
            color_scheme_seed=light_colors['primary'],
            color_scheme=ft.ColorScheme(
                primary=light_colors['primary'],
                on_primary=light_colors['on_primary'],
                primary_container=light_colors['primary_container'],
                on_primary_container=light_colors['on_primary_container'],
                secondary=light_colors['secondary'],
                on_secondary=light_colors['on_secondary'],
                secondary_container=light_colors['secondary_container'],
                on_secondary_container=light_colors['on_secondary_container'],
                background=light_colors['background'],
                on_background=light_colors['on_background'],
                surface=light_colors['surface'],
                on_surface=light_colors['on_surface'],
                surface_variant=light_colors['surface_variant'],
                on_surface_variant=light_colors['on_surface_variant'],
                outline=light_colors['outline'],
                error=light_colors['error'],
                on_error=light_colors['on_error'],
            ),
        )
        
        # Set dark mode by default
        self.page.theme_mode = ft.ThemeMode.DARK
    
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
        
        # Create theme toggle button
        self.theme_toggle = ft.IconButton(
            icon=ft.icons.DARK_MODE if self.is_dark_mode else ft.icons.LIGHT_MODE,
            icon_size=20,
            tooltip="Toggle Light/Dark Mode",
            on_click=self._toggle_theme,
        )
        
        # Create header with title and theme toggle
        header = ft.Container(
            content=ft.Row([
                ft.Text("Graph Creator", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.theme_toggle], spacing=0),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        
        # Create main layout
        main_content = ft.Row([
            self.builder,
            ft.VerticalDivider(width=1),
            self.canvas,
        ], spacing=0, expand=True)
        
        # Add everything to page
        self.page.add(
            ft.Column([
                header,
                main_content,
            ], spacing=0, expand=True)
        )
    
    def _toggle_theme(self, e):
        """Toggle between light and dark modes."""
        self.is_dark_mode = not self.is_dark_mode
        
        if self.is_dark_mode:
            self.page.theme_mode = ft.ThemeMode.DARK
            self.theme_toggle.icon = ft.icons.DARK_MODE
            # Update chart theme to dark
            from .models.data_models import Theme
            self.state.theme = Theme(
                name="dark",
                mode="dark",
                background_color="#0C1A26",
                grid_color="#18324A",
                text_color="#E8EEF3",
                color_palette=[
                    "#3A82F7", "#4E9FB9", "#3DBE8B", "#E3A65A", "#C05555",
                    "#7B61FF", "#FF6B9D", "#FFB84D", "#4ECDC4", "#95E1D3"
                ],
            )
        else:
            self.page.theme_mode = ft.ThemeMode.LIGHT
            self.page.theme = self.light_theme
            self.theme_toggle.icon = ft.icons.LIGHT_MODE
            # Update chart theme to light
            from .models.data_models import Theme
            self.state.theme = Theme(
                name="light",
                mode="light",
                background_color="#F6F9FB",
                grid_color="#E4EBF0",
                text_color="#1E2B36",
                color_palette=[
                    "#2F6BDB", "#5FA7D3", "#2C8C64", "#C97A2C", "#B23C3C",
                    "#6B4EFF", "#FF4D7D", "#FF9B3D", "#3EAAA0", "#75C9B9"
                ],
            )
        
        # Re-render the chart with new theme
        self._refresh_ui()
    
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
        # Save snapshot is handled by individual handlers that need it
        # Always render for real-time updates
        self.canvas.render()
        # Update page to show changes
        self.page.update()
    
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
                
            elif example_type == "blank":
                # Create a blank chart with minimal example data
                data_source = DataLoader.create_blank_data()
                self.state.data_source = data_source
                self.state.chart_config = ChartConfig(
                    chart_type="line",
                    title="New Graph",
                    subtitle="",
                    x_column="X",  # Set default X column
                )
                # Explicitly clear any auto-created series for blank charts
                self.state.chart_config.series_styles.clear()
            
            self.state.save_snapshot()
            self._refresh_ui()
            
            if example_type != "blank":
                self._show_success("Example Loaded", f"Loaded {example_type} example successfully")
            else:
                self._show_success("Blank Graph", "Created new blank graph. Import data to begin.")
        
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
        elif source_type == "export_csv":
            self._export_data()
    
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


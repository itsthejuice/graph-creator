"""Canvas/Preview UI component."""

import flet as ft
from typing import Optional
import io
import base64

from ..models.state import AppState
from ..charts.mpl_renderer import MatplotlibRenderer


class Canvas(ft.Container):
    """Right pane canvas/preview panel."""
    
    def __init__(
        self,
        state: AppState,
        on_export: callable,
        **kwargs
    ):
        self.state = state
        self.on_export = on_export
        self.renderer = MatplotlibRenderer()
        self.current_metadata = {}
        
        # Build UI
        self.chart_image = ft.Image(
            src_base64="",
            fit=ft.ImageFit.CONTAIN,
            repeat=ft.ImageRepeat.NO_REPEAT,
            visible=False,
        )
        
        self.placeholder_text = ft.Container(
            content=ft.Column([
                ft.Icon(ft.icons.INSERT_CHART_OUTLINED, size=64, color=ft.colors.OUTLINE),
                ft.Text("No data loaded", size=16, color=ft.colors.OUTLINE),
                ft.Text("Load an example or import data", size=12, color=ft.colors.OUTLINE),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            alignment=ft.alignment.center,
        )
        
        self.status_bar = ft.Container(
            content=ft.Row([
                ft.Text("Ready", size=11),
            ]),
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=8,
        )
        
        self.chart_container = ft.Stack([
            self.placeholder_text,
            self.chart_image,
        ], expand=True)
        
        content = ft.Column([
            self._build_toolbar(),
            ft.Container(
                content=self.chart_container,
                expand=True,
                alignment=ft.alignment.center,
                bgcolor=ft.colors.SURFACE,
            ),
            self.status_bar,
        ], spacing=0)
        
        super().__init__(
            content=content,
            expand=True,
            **kwargs
        )
    
    def _build_toolbar(self) -> ft.Control:
        """Build toolbar with export options."""
        return ft.Container(
            content=ft.Row([
                ft.Text("Preview", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.REFRESH,
                        tooltip="Refresh Preview",
                        on_click=lambda _: self.render(),
                    ),
                    ft.PopupMenuButton(
                        icon=ft.icons.DOWNLOAD,
                        tooltip="Export",
                        items=[
                            ft.PopupMenuItem(
                                text="Export PNG",
                                on_click=lambda _: self.on_export("png"),
                            ),
                            ft.PopupMenuItem(
                                text="Export SVG",
                                on_click=lambda _: self.on_export("svg"),
                            ),
                            ft.PopupMenuItem(
                                text="Export PDF",
                                on_click=lambda _: self.on_export("pdf"),
                            ),
                            ft.PopupMenuItem(
                                text="Export Data (CSV)",
                                on_click=lambda _: self.on_export("csv"),
                            ),
                        ],
                    ),
                ], spacing=0),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=10,
        )
    
    def render(self):
        """Render the chart."""
        try:
            # Get transformed data
            df = self.state.get_transformed_data()
            
            if df is None or len(df) == 0:
                self._show_placeholder("No data to display")
                return
            
            # Render chart
            fig, metadata = self.renderer.render(
                df,
                self.state.chart_config,
                self.state.theme,
            )
            
            self.current_metadata = metadata
            
            # Convert to image
            img_bytes = self.renderer.save_to_bytes(format='png', dpi=100)
            
            # Convert to base64 for display
            img_base64 = base64.b64encode(img_bytes).decode()
            self.chart_image.src_base64 = img_base64
            self.chart_image.visible = True
            self.placeholder_text.visible = False
            
            # Update status bar
            self._update_status(metadata)
            
            # Clean up
            self.renderer.close()
            
            # Update UI
            if hasattr(self, 'update'):
                self.update()
        
        except Exception as e:
            self._show_error(str(e))
    
    def _show_placeholder(self, message: str):
        """Show placeholder message."""
        self.chart_image.visible = False
        self.placeholder_text.visible = True
        self.status_bar.content = ft.Row([
            ft.Icon(ft.icons.INFO_OUTLINE, size=16),
            ft.Text(message, size=11),
        ])
        
        if hasattr(self, 'update'):
            self.update()
    
    def _show_error(self, error: str):
        """Show error message."""
        self.chart_image.visible = False
        self.placeholder_text.visible = True
        self.status_bar.content = ft.Row([
            ft.Icon(ft.icons.ERROR_OUTLINE, size=16, color=ft.colors.ERROR),
            ft.Text(f"Error: {error}", size=11, color=ft.colors.ERROR),
        ])
        
        if hasattr(self, 'update'):
            self.update()
    
    def _update_status(self, metadata: dict):
        """Update status bar with metadata."""
        rows = metadata.get("rows", 0)
        render_time = metadata.get("render_time", 0)
        warnings = metadata.get("warnings", [])
        
        status_text = f"{rows} rows • {render_time:.2f}s"
        
        if warnings:
            status_text += f" • {len(warnings)} warning(s)"
        
        self.status_bar.content = ft.Row([
            ft.Icon(ft.icons.CHECK_CIRCLE, size=16, color=ft.colors.GREEN),
            ft.Text(status_text, size=11),
        ])
        
        if hasattr(self, 'update'):
            self.update()
    
    def export_image(self, file_path: str, format: str = "png", dpi: int = 300):
        """Export current chart to file."""
        try:
            df = self.state.get_transformed_data()
            
            if df is None:
                return False
            
            # Re-render at high DPI
            fig, _ = self.renderer.render(
                df,
                self.state.chart_config,
                self.state.theme,
            )
            
            # Save
            self.renderer.save_to_file(file_path, dpi=dpi)
            self.renderer.close()
            
            return True
        
        except Exception as e:
            print(f"Export error: {e}")
            return False


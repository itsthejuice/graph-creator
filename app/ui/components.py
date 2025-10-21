"""Reusable UI components."""

import flet as ft
from typing import Callable, Optional, List, Any


class Section(ft.Container):
    """Collapsible section container."""
    
    def __init__(
        self,
        title: str,
        content: ft.Control,
        expanded: bool = True,
        **kwargs
    ):
        self.title_text = title
        self.content_control = content
        self.is_expanded = expanded
        
        self.header = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.icons.EXPAND_MORE if expanded else ft.icons.CHEVRON_RIGHT,
                    size=20,
                ),
                ft.Text(title, weight=ft.FontWeight.BOLD, size=14),
            ]),
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=8,
            border_radius=4,
            on_click=self._toggle,
        )
        
        self.body = ft.Container(
            content=content,
            padding=ft.padding.only(left=10, right=10, top=5, bottom=10),
            visible=expanded,
        )
        
        super().__init__(
            content=ft.Column([
                self.header,
                self.body,
            ], spacing=0),
            **kwargs
        )
    
    def _toggle(self, e):
        """Toggle section expansion."""
        self.is_expanded = not self.is_expanded
        self.body.visible = self.is_expanded
        
        # Update icon
        icon = self.header.content.controls[0]
        icon.name = ft.icons.EXPAND_MORE if self.is_expanded else ft.icons.CHEVRON_RIGHT
        
        self.update()


class LabeledControl(ft.Row):
    """Control with label."""
    
    def __init__(
        self,
        label: str,
        control: ft.Control,
        help_text: str = "",
        **kwargs
    ):
        controls = [
            ft.Container(
                content=ft.Text(label, size=12, weight=ft.FontWeight.W_500),
                width=120,
            ),
            ft.Container(
                content=control,
                expand=True,
            ),
        ]
        
        if help_text:
            controls.append(
                ft.Tooltip(
                    message=help_text,
                    content=ft.Icon(ft.icons.HELP_OUTLINE, size=16),
                )
            )
        
        super().__init__(
            controls=controls,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            **kwargs
        )


class DataTable(ft.Container):
    """Simple data table component."""
    
    def __init__(
        self,
        columns: List[str],
        rows: List[List[Any]],
        on_cell_edit: Optional[Callable] = None,
        height: int = 300,
        **kwargs
    ):
        self.column_names = columns
        self.data_rows = rows
        self.on_cell_edit = on_cell_edit
        
        # Create header
        header = ft.Row([
            ft.Container(
                content=ft.Text(col, weight=ft.FontWeight.BOLD, size=12),
                bgcolor=ft.colors.SURFACE_VARIANT,
                padding=5,
                expand=True,
            )
            for col in columns
        ], spacing=1)
        
        # Create rows
        row_controls = []
        for row_idx, row_data in enumerate(rows[:50]):  # Limit to 50 rows for performance
            row_cells = []
            for col_idx, cell_value in enumerate(row_data):
                row_cells.append(
                    ft.Container(
                        content=ft.Text(str(cell_value), size=11),
                        padding=5,
                        expand=True,
                        bgcolor=ft.colors.SURFACE if row_idx % 2 == 0 else None,
                    )
                )
            row_controls.append(ft.Row(row_cells, spacing=1))
        
        content = ft.Column([
            header,
            ft.Container(
                content=ft.Column(row_controls, spacing=1, scroll=ft.ScrollMode.AUTO),
                height=height,
            ),
        ], spacing=1)
        
        super().__init__(
            content=content,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=4,
            **kwargs
        )


class ColorPicker(ft.Container):
    """Simple color picker."""
    
    def __init__(
        self,
        value: str = "#1f77b4",
        on_change: Optional[Callable] = None,
        **kwargs
    ):
        self.color_value = value
        self.on_change_callback = on_change
        
        self.color_display = ft.Container(
            width=30,
            height=30,
            bgcolor=value,
            border_radius=4,
            border=ft.border.all(1, ft.colors.OUTLINE),
        )
        
        self.text_field = ft.TextField(
            value=value,
            width=100,
            height=40,
            text_size=12,
            on_change=self._on_text_change,
        )
        
        super().__init__(
            content=ft.Row([
                self.color_display,
                self.text_field,
            ], spacing=5),
            **kwargs
        )
    
    def _on_text_change(self, e):
        """Handle text field change."""
        self.color_value = e.control.value
        self.color_display.bgcolor = e.control.value
        self.color_display.update()
        
        if self.on_change_callback:
            self.on_change_callback(e)
    
    @property
    def value(self) -> str:
        """Get current color value."""
        return self.color_value
    
    @value.setter
    def value(self, val: str):
        """Set color value."""
        self.color_value = val
        self.color_display.bgcolor = val
        self.text_field.value = val
        if hasattr(self, 'update'):
            self.update()


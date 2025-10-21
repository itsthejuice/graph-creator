"""Builder sidebar UI component."""

import flet as ft
from typing import Callable, Optional
import pandas as pd

from ..models.state import AppState
from ..models.data_models import SeriesStyle, AxisConfig, Annotation, Transform
from .components import Section, LabeledControl, ColorPicker


class Builder(ft.Container):
    """Left sidebar builder panel."""
    
    def __init__(
        self,
        state: AppState,
        on_change: Callable,
        on_load_example: Callable,
        on_import_data: Callable,
        **kwargs
    ):
        self.state = state
        self.on_change = on_change
        self.on_load_example = on_load_example
        self.on_import_data = on_import_data
        self.page = None  # Will be set by parent
        
        # Track section expansion states
        self.section_expanded = {
            0: True,   # Data Sources
            1: True,   # Data Editor
            2: True,   # Chart Type
            3: True,   # Series
            4: True,   # Axes & Scales
            5: True,   # Layout & Labels
            6: False,  # Annotations
            7: False,  # Theme & Styling
        }
        
        # Create scrollable column for sections (stores reference for dynamic updates)
        self.sections_column = ft.Column([
            self._build_data_section(),
            self._build_data_preview_section(),
            self._build_chart_type_section(),
            self._build_series_section(),
            self._build_axes_section(),
            self._build_layout_section(),
            self._build_annotations_section(),
            self._build_theme_section(),
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        # Build UI
        content = ft.Column([
            self._build_header(),
            ft.Divider(),
            ft.Container(
                content=self.sections_column,
                expand=True,
            ),
        ], spacing=0)
        
        super().__init__(
            content=content,
            width=350,
            bgcolor=ft.colors.SURFACE,
            padding=10,
            **kwargs
        )
    
    def _build_header(self) -> ft.Control:
        """Build header with title and actions."""
        return ft.Row([
            ft.Text("Builder", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.IconButton(
                    icon=ft.icons.FOLDER_OPEN,
                    tooltip="Open Project",
                    on_click=lambda _: self.on_import_data("project"),
                ),
                ft.IconButton(
                    icon=ft.icons.SAVE,
                    tooltip="Save Project (Ctrl+S)",
                    on_click=lambda _: self.on_change(),
                ),
            ], spacing=0),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    
    def _build_data_section(self) -> ft.Control:
        """Build data sources section."""
        new_graph_btn = ft.ElevatedButton(
            "New Blank Graph",
            icon=ft.icons.ADD_CHART,
            on_click=lambda _: self.on_load_example("blank"),
        )
        
        examples_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    text="Overlapping Trends",
                    on_click=lambda _: self.on_load_example("overlapping"),
                ),
                ft.PopupMenuItem(
                    text="Economic Indicators",
                    on_click=lambda _: self.on_load_example("economic"),
                ),
                ft.PopupMenuItem(
                    text="Contamination vs Rawness",
                    on_click=lambda _: self.on_load_example("contamination"),
                ),
            ],
            icon=ft.icons.LIGHTBULB_OUTLINE,
            tooltip="Load Example",
        )
        
        import_menu = ft.PopupMenuButton(
            items=[
                ft.PopupMenuItem(
                    text="Import CSV",
                    on_click=lambda _: self.on_import_data("csv"),
                ),
                ft.PopupMenuItem(
                    text="Import JSON",
                    on_click=lambda _: self.on_import_data("json"),
                ),
                ft.PopupMenuItem(
                    text="Paste from Clipboard",
                    on_click=lambda _: self.on_import_data("clipboard"),
                ),
            ],
            icon=ft.icons.UPLOAD_FILE,
            tooltip="Import Data",
        )
        
        data_info = ft.Text(
            self._get_data_info(),
            size=11,
            color=ft.colors.ON_SURFACE_VARIANT,
        )
        
        content = ft.Column([
            new_graph_btn,
            ft.Row([
                examples_menu,
                import_menu,
            ], alignment=ft.MainAxisAlignment.START),
            data_info,
        ], spacing=5)
        
        return Section("Data Sources", content, expanded=self.section_expanded.get(0, True))
    
    def _get_data_info(self) -> str:
        """Get data source info text."""
        if self.state.data_source is None:
            return "No data loaded. Load an example or import data."
        
        df = self.state.get_transformed_data()
        if df is None:
            return "No data available."
        
        return f"{len(df)} rows × {len(df.columns)} columns"
    
    def _build_data_preview_section(self) -> ft.Control:
        """Build editable data table section."""
        if self.state.data_source is None:
            return Section("Data Editor", ft.Text("No data loaded", size=11), expanded=self.section_expanded.get(1, False))
        
        df = self.state.data_source.df  # Use original data, not transformed
        if df is None or len(df) == 0:
            return Section("Data Editor", ft.Text("No data available", size=11), expanded=self.section_expanded.get(1, False))
        
        # Control buttons
        controls_row = ft.Row([
            ft.ElevatedButton(
                "Add Row",
                icon=ft.icons.ADD,
                on_click=self._on_add_row,
                height=35,
            ),
            ft.ElevatedButton(
                "Delete Last Row",
                icon=ft.icons.REMOVE,
                on_click=self._on_delete_row,
                height=35,
            ),
            ft.ElevatedButton(
                "Add Column",
                icon=ft.icons.VIEW_COLUMN,
                on_click=self._on_add_column,
                height=35,
            ),
            ft.ElevatedButton(
                "Export CSV",
                icon=ft.icons.DOWNLOAD,
                on_click=self._on_export_data_csv,
                height=35,
            ),
        ], spacing=5, wrap=True)
        
        # Limit display to avoid performance issues
        max_display_rows = min(10, len(df))
        max_display_cols = min(6, len(df.columns))
        
        # Build editable table
        table_rows = []
        
        # Header row with column names (editable)
        header_cells = [ft.Container(content=ft.Text("Row", size=9, weight=ft.FontWeight.BOLD), width=40, padding=3, bgcolor=ft.colors.SURFACE_VARIANT)]
        for col_idx, col in enumerate(df.columns[:max_display_cols]):
            header_cells.append(
                ft.Container(
                    content=ft.TextField(
                        value=str(col),
                        on_submit=lambda e, idx=col_idx: self._on_column_rename(e, idx),
                        on_blur=lambda e, idx=col_idx: self._on_column_rename(e, idx),
                        text_size=9,
                        height=35,
                        dense=True,
                        content_padding=3,
                        border_color=ft.colors.OUTLINE,
                    ),
                    width=100,
                    padding=2,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                )
            )
        
        # Add delete column buttons
        for col_idx in range(max_display_cols):
            col = df.columns[col_idx]
            header_cells.append(
                ft.Container(
                    content=ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_size=14,
                        tooltip=f"Delete column '{col}'",
                        on_click=lambda _, idx=col_idx: self._on_delete_column(idx),
                    ),
                    width=30,
                    padding=0,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                )
            )
            break  # Only add delete button once in header
        
        table_rows.append(ft.Row(header_cells, spacing=1))
        
        # Data rows (editable)
        for row_idx in range(max_display_rows):
            row_cells = [
                ft.Container(
                    content=ft.Text(str(row_idx), size=9, weight=ft.FontWeight.BOLD),
                    width=40,
                    padding=3,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                )
            ]
            
            for col_idx, col in enumerate(df.columns[:max_display_cols]):
                cell_value = df.iloc[row_idx, col_idx]
                row_cells.append(
                    ft.Container(
                        content=ft.TextField(
                            value=str(cell_value) if cell_value is not None else "",
                            on_submit=lambda e, r=row_idx, c=col_idx: self._on_cell_edit(e, r, c),
                            on_blur=lambda e, r=row_idx, c=col_idx: self._on_cell_edit(e, r, c),
                            text_size=9,
                            height=35,
                            dense=True,
                            content_padding=3,
                            border_color=ft.colors.OUTLINE,
                        ),
                        width=100,
                        padding=2,
                        bgcolor=ft.colors.SURFACE if row_idx % 2 == 0 else None,
                    )
                )
            
            table_rows.append(ft.Row(row_cells, spacing=1, scroll=ft.ScrollMode.AUTO))
        
        table_info = ft.Text(
            f"Showing {max_display_rows} of {len(df)} rows, {max_display_cols} of {len(df.columns)} columns (editable)",
            size=9,
            italic=True,
            color=ft.colors.ON_SURFACE_VARIANT,
        )
        
        content = ft.Column([
            controls_row,
            ft.Divider(height=1),
            table_info,
            ft.Container(
                content=ft.Column(table_rows, spacing=1, scroll=ft.ScrollMode.AUTO),
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=4,
                height=400,  # Fixed height with scrolling
            ),
        ], spacing=5)
        
        return Section("Data Editor", content, expanded=self.section_expanded.get(1, False))
    
    def _build_chart_type_section(self) -> ft.Control:
        """Build chart type selection."""
        chart_type = ft.Dropdown(
            options=[
                ft.dropdown.Option("line", "Line"),
                ft.dropdown.Option("area", "Area"),
                ft.dropdown.Option("bar", "Bar"),
                ft.dropdown.Option("stacked_bar", "Stacked Bar"),
                ft.dropdown.Option("bar_100", "100% Bar"),
                ft.dropdown.Option("scatter", "Scatter"),
                ft.dropdown.Option("step", "Step"),
                ft.dropdown.Option("histogram", "Histogram"),
                ft.dropdown.Option("kde", "KDE"),
                ft.dropdown.Option("box", "Box Plot"),
                ft.dropdown.Option("violin", "Violin Plot"),
            ],
            value=self.state.chart_config.chart_type,
            on_change=self._on_chart_type_change,
            height=60,
            text_size=13,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
            bgcolor=ft.colors.SURFACE_VARIANT,
            color=ft.colors.ON_SURFACE,
            border_color=ft.colors.OUTLINE,
        )
        
        content = ft.Column([
            LabeledControl("Type", chart_type),
        ])
        
        return Section("Chart Type", content, expanded=self.section_expanded.get(2, True))
    
    def _on_chart_type_change(self, e):
        """Handle chart type change."""
        self.state.chart_config.chart_type = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _build_series_section(self) -> ft.Control:
        """Build series configuration."""
        if self.state.data_source is None:
            return Section("Series", ft.Text("No data loaded", size=11))
        
        df = self.state.get_transformed_data()
        if df is None:
            return Section("Series", ft.Text("No data available", size=11))
        
        # X column selector
        x_column = ft.Dropdown(
            options=[ft.dropdown.Option(col, col) for col in df.columns],
            value=self.state.chart_config.x_column,
            on_change=self._on_x_column_change,
            label="X Column",
            height=60,
            text_size=13,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
            bgcolor=ft.colors.SURFACE_VARIANT,
            color=ft.colors.ON_SURFACE,
            border_color=ft.colors.OUTLINE,
        )
        
        # Auto-create series styles if needed (but not for blank data)
        if not self.state.chart_config.series_styles and self.state.data_source.name != "Blank":
            self._auto_create_series()
        
        # Add series button
        add_series_btn = ft.ElevatedButton(
            "Add Series",
            icon=ft.icons.ADD,
            on_click=self._on_add_series,
            height=35,
        )
        
        # Series list
        series_controls = []
        for i, series in enumerate(self.state.chart_config.series_styles):
            series_controls.append(
                self._build_series_control(series, i)
            )
        
        content = ft.Column([
            x_column,
            add_series_btn,
            ft.Divider(),
            *series_controls,
        ], spacing=10)
        
        return Section("Series", content, expanded=self.section_expanded.get(3, True))
    
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
        
        # Create series styles
        for col in numeric_cols[:10]:  # Limit to 10 series
            self.state.chart_config.series_styles.append(
                SeriesStyle(column=col, visible=True)
            )
    
    def _build_series_control(self, series: SeriesStyle, index: int) -> ft.Control:
        """Build control for single series."""
        # Get available columns for dropdown
        df = self.state.get_transformed_data()
        available_columns = list(df.columns) if df is not None else [series.column]
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Checkbox(
                        value=series.visible,
                        on_change=lambda e, idx=index: self._on_series_visible_change(e, idx),
                    ),
                    ft.Text(series.label if series.label else series.column, size=12, weight=ft.FontWeight.W_500, expand=True),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_size=18,
                        tooltip="Remove series",
                        on_click=lambda _, idx=index: self._on_delete_series(idx),
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(
                    content=ft.Column([
                        LabeledControl(
                            "Data Column",
                            ft.Dropdown(
                                options=[ft.dropdown.Option(col, col) for col in available_columns],
                                value=series.column,
                                on_change=lambda e, idx=index: self._on_series_column_change(e, idx),
                                height=55,
                                text_size=12,
                                content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                color=ft.colors.ON_SURFACE,
                                border_color=ft.colors.OUTLINE,
                            ),
                        ),
                        LabeledControl(
                            "Label",
                            ft.TextField(
                                value=series.label if series.label else series.column,
                                on_change=lambda e, idx=index: self._on_series_label_change(e, idx),
                                height=50,
                                text_size=13,
                                content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                color=ft.colors.ON_SURFACE,
                                border_color=ft.colors.OUTLINE,
                            ),
                        ),
                        ft.Column([
                            ft.Text("Color", size=12, weight=ft.FontWeight.W_500),
                            ft.Row([
                                ft.Container(
                                    width=30,
                                    height=30,
                                    bgcolor=series.color if series.color else self.state.theme.color_palette[index % len(self.state.theme.color_palette)],
                                    border_radius=4,
                                    border=ft.border.all(1, ft.colors.OUTLINE),
                                ),
                                ft.TextField(
                                    value=series.color if series.color else self.state.theme.color_palette[index % len(self.state.theme.color_palette)],
                                    on_change=lambda e, idx=index: self._on_series_color_change(e, idx),
                                    hint_text="#RRGGBB",
                                    height=50,
                                    text_size=12,
                                    expand=True,
                                    content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                                    bgcolor=ft.colors.SURFACE_VARIANT,
                                    color=ft.colors.ON_SURFACE,
                                    border_color=ft.colors.OUTLINE,
                                ),
                            ], spacing=5),
                        ], spacing=5),
                        LabeledControl(
                            "Line Width",
                            ft.Slider(
                                min=0.5,
                                max=5,
                                value=series.line_width,
                                on_change=lambda e, idx=index: self._on_series_width_change(e, idx),
                            ),
                        ),
                        LabeledControl(
                            "Line Style",
                            ft.Dropdown(
                                options=[
                                    ft.dropdown.Option("solid", "Solid"),
                                    ft.dropdown.Option("dashed", "Dashed"),
                                    ft.dropdown.Option("dotted", "Dotted"),
                                    ft.dropdown.Option("dashdot", "Dash-Dot"),
                                ],
                                value=series.line_style,
                                on_change=lambda e, idx=index: self._on_series_style_change(e, idx),
                                height=55,
                                text_size=12,
                                content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                color=ft.colors.ON_SURFACE,
                                border_color=ft.colors.OUTLINE,
                            ),
                        ),
                        LabeledControl(
                            "Marker",
                            ft.Dropdown(
                                options=[
                                    ft.dropdown.Option("", "None"),
                                    ft.dropdown.Option("o", "Circle"),
                                    ft.dropdown.Option("s", "Square"),
                                    ft.dropdown.Option("^", "Triangle Up"),
                                    ft.dropdown.Option("v", "Triangle Down"),
                                    ft.dropdown.Option("D", "Diamond"),
                                    ft.dropdown.Option("*", "Star"),
                                    ft.dropdown.Option("+", "Plus"),
                                    ft.dropdown.Option("x", "X"),
                                ],
                                value=series.marker,
                                on_change=lambda e, idx=index: self._on_series_marker_change(e, idx),
                                height=55,
                                text_size=12,
                                content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                color=ft.colors.ON_SURFACE,
                                border_color=ft.colors.OUTLINE,
                            ),
                        ),
                        LabeledControl(
                            "Marker Size",
                            ft.Slider(
                                min=2,
                                max=15,
                                value=series.marker_size,
                                on_change=lambda e, idx=index: self._on_series_marker_size_change(e, idx),
                            ),
                        ),
                        LabeledControl(
                            "Transparency",
                            ft.Slider(
                                min=0.1,
                                max=1.0,
                                value=series.alpha,
                                on_change=lambda e, idx=index: self._on_series_alpha_change(e, idx),
                                divisions=9,
                            ),
                        ),
                        LabeledControl(
                            "Y Axis",
                            ft.Dropdown(
                                options=[
                                    ft.dropdown.Option("primary", "Primary"),
                                    ft.dropdown.Option("secondary", "Secondary"),
                                ],
                                value=series.y_axis,
                                on_change=lambda e, idx=index: self._on_series_axis_change(e, idx),
                                height=55,
                                text_size=12,
                                content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                color=ft.colors.ON_SURFACE,
                                border_color=ft.colors.OUTLINE,
                            ),
                        ),
                    ], spacing=5),
                    padding=ft.padding.only(left=30),
                    visible=series.visible,
                ),
            ], spacing=5),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=4,
            padding=10,
        )
    
    def _on_x_column_change(self, e):
        """Handle X column change."""
        self.state.chart_config.x_column = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_visible_change(self, e, index: int):
        """Handle series visibility change."""
        self.state.chart_config.series_styles[index].visible = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_width_change(self, e, index: int):
        """Handle series line width change."""
        self.state.chart_config.series_styles[index].line_width = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_style_change(self, e, index: int):
        """Handle series line style change."""
        self.state.chart_config.series_styles[index].line_style = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_axis_change(self, e, index: int):
        """Handle series axis change."""
        self.state.chart_config.series_styles[index].y_axis = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_column_change(self, e, index: int):
        """Handle series data column change."""
        self.state.chart_config.series_styles[index].column = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_label_change(self, e, index: int):
        """Handle series label change."""
        self.state.chart_config.series_styles[index].label = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_color_change(self, e, index: int):
        """Handle series color change."""
        color_value = e.control.value if e.control.value else None
        self.state.chart_config.series_styles[index].color = color_value
        self.state.save_snapshot()
        # Rebuild series section to update color preview
        self._rebuild_section(3)
        self.on_change()
    
    def _on_series_marker_change(self, e, index: int):
        """Handle series marker change."""
        self.state.chart_config.series_styles[index].marker = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_marker_size_change(self, e, index: int):
        """Handle series marker size change."""
        self.state.chart_config.series_styles[index].marker_size = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_series_alpha_change(self, e, index: int):
        """Handle series transparency change."""
        self.state.chart_config.series_styles[index].alpha = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_add_series(self, e):
        """Add a new series."""
        df = self.state.get_transformed_data()
        if df is None:
            return
        
        # Get available columns (those not already in series)
        existing_columns = {s.column for s in self.state.chart_config.series_styles}
        x_col = self.state.chart_config.x_column
        available_cols = [col for col in df.columns if col not in existing_columns and col != x_col]
        
        if available_cols:
            # Add the first available column
            self.state.chart_config.series_styles.append(
                SeriesStyle(column=available_cols[0], visible=True)
            )
            self.state.save_snapshot()
            # Rebuild the series section only
            self._rebuild_section(2)  # Series section is at index 2
            self.on_change()
    
    def _on_delete_series(self, index: int):
        """Delete a series."""
        if len(self.state.chart_config.series_styles) > 0:
            self.state.chart_config.series_styles.pop(index)
            self.state.save_snapshot()
            # Rebuild the series section only
            self._rebuild_section(3)  # Series section is at index 3
            self.on_change()
    
    def _build_axes_section(self) -> ft.Control:
        """Build axes configuration."""
        content = ft.Column([
            ft.Text("X Axis", size=12, weight=ft.FontWeight.BOLD),
            LabeledControl(
                "Label",
                ft.TextField(
                    value=self.state.chart_config.x_axis.label,
                    on_change=self._on_x_label_change,
                    height=50,
                    text_size=13,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
            LabeledControl(
                "Scale",
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("linear", "Linear"),
                        ft.dropdown.Option("log", "Logarithmic"),
                    ],
                    value=self.state.chart_config.x_axis.scale,
                    on_change=self._on_x_scale_change,
                    height=55,
                    text_size=12,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
            ft.Column([
                ft.Text("Range", size=11, weight=ft.FontWeight.W_500),
                ft.Row([
                    ft.TextField(
                        value=str(self.state.chart_config.x_axis.min_value) if self.state.chart_config.x_axis.min_value is not None else "",
                        on_change=self._on_x_min_change,
                        hint_text="Min",
                        label="Min",
                        height=50,
                        text_size=12,
                        expand=True,
                        content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.ON_SURFACE,
                        border_color=ft.colors.OUTLINE,
                    ),
                    ft.TextField(
                        value=str(self.state.chart_config.x_axis.max_value) if self.state.chart_config.x_axis.max_value is not None else "",
                        on_change=self._on_x_max_change,
                        hint_text="Max",
                        label="Max",
                        height=50,
                        text_size=12,
                        expand=True,
                        content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.ON_SURFACE,
                        border_color=ft.colors.OUTLINE,
                    ),
                ], spacing=5),
            ], spacing=5),
            ft.Divider(),
            ft.Text("Primary Y Axis", size=12, weight=ft.FontWeight.BOLD),
            LabeledControl(
                "Label",
                ft.TextField(
                    value=self.state.chart_config.y_axis_primary.label,
                    on_change=self._on_y_label_change,
                    height=50,
                    text_size=13,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
            LabeledControl(
                "Scale",
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("linear", "Linear"),
                        ft.dropdown.Option("log", "Logarithmic"),
                    ],
                    value=self.state.chart_config.y_axis_primary.scale,
                    on_change=self._on_y_scale_change,
                    height=55,
                    text_size=12,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
            LabeledControl(
                "Grid",
                ft.Switch(
                    value=self.state.chart_config.y_axis_primary.show_grid,
                    on_change=self._on_grid_change,
                ),
            ),
            ft.Column([
                ft.Text("Range", size=11, weight=ft.FontWeight.W_500),
                ft.Row([
                    ft.TextField(
                        value=str(self.state.chart_config.y_axis_primary.min_value) if self.state.chart_config.y_axis_primary.min_value is not None else "",
                        on_change=self._on_y_min_change,
                        hint_text="Min",
                        label="Min",
                        height=50,
                        text_size=12,
                        expand=True,
                        content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.ON_SURFACE,
                        border_color=ft.colors.OUTLINE,
                    ),
                    ft.TextField(
                        value=str(self.state.chart_config.y_axis_primary.max_value) if self.state.chart_config.y_axis_primary.max_value is not None else "",
                        on_change=self._on_y_max_change,
                        hint_text="Max",
                        label="Max",
                        height=50,
                        text_size=12,
                        expand=True,
                        content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.ON_SURFACE,
                        border_color=ft.colors.OUTLINE,
                    ),
                ], spacing=5),
            ], spacing=5),
        ], spacing=10)
        
        # Add secondary Y axis if any series uses it
        has_secondary = any(
            s.y_axis == "secondary" and s.visible 
            for s in self.state.chart_config.series_styles
        )
        
        if has_secondary:
            # Ensure secondary axis config exists
            if self.state.chart_config.y_axis_secondary is None:
                from ..models.data_models import AxisConfig
                self.state.chart_config.y_axis_secondary = AxisConfig()
            
            content.controls.extend([
                ft.Divider(),
                ft.Text("Secondary Y Axis", size=12, weight=ft.FontWeight.BOLD),
                LabeledControl(
                    "Label",
                    ft.TextField(
                        value=self.state.chart_config.y_axis_secondary.label,
                        on_change=self._on_y2_label_change,
                        height=50,
                        text_size=13,
                        content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.ON_SURFACE,
                        border_color=ft.colors.OUTLINE,
                    ),
                ),
                LabeledControl(
                    "Scale",
                    ft.Dropdown(
                        options=[
                            ft.dropdown.Option("linear", "Linear"),
                            ft.dropdown.Option("log", "Logarithmic"),
                        ],
                        value=self.state.chart_config.y_axis_secondary.scale,
                        on_change=self._on_y2_scale_change,
                        height=55,
                        text_size=12,
                        content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                        bgcolor=ft.colors.SURFACE_VARIANT,
                        color=ft.colors.ON_SURFACE,
                        border_color=ft.colors.OUTLINE,
                    ),
                ),
            ])
        
        return Section("Axes & Scales", content, expanded=self.section_expanded.get(4, True))
    
    def _on_x_label_change(self, e):
        """Handle X label change."""
        self.state.chart_config.x_axis.label = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_x_scale_change(self, e):
        """Handle X scale change."""
        self.state.chart_config.x_axis.scale = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_x_min_change(self, e):
        """Handle X min change."""
        try:
            val = float(e.control.value) if e.control.value else None
            self.state.chart_config.x_axis.min_value = val
            self.state.save_snapshot()
            self.on_change()
        except ValueError:
            pass
    
    def _on_x_max_change(self, e):
        """Handle X max change."""
        try:
            val = float(e.control.value) if e.control.value else None
            self.state.chart_config.x_axis.max_value = val
            self.state.save_snapshot()
            self.on_change()
        except ValueError:
            pass
    
    def _on_y_label_change(self, e):
        """Handle Y label change."""
        self.state.chart_config.y_axis_primary.label = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_y_scale_change(self, e):
        """Handle Y scale change."""
        self.state.chart_config.y_axis_primary.scale = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_grid_change(self, e):
        """Handle grid toggle."""
        self.state.chart_config.y_axis_primary.show_grid = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_y_min_change(self, e):
        """Handle Y min change."""
        try:
            val = float(e.control.value) if e.control.value else None
            self.state.chart_config.y_axis_primary.min_value = val
            self.state.save_snapshot()
            self.on_change()
        except ValueError:
            pass
    
    def _on_y_max_change(self, e):
        """Handle Y max change."""
        try:
            val = float(e.control.value) if e.control.value else None
            self.state.chart_config.y_axis_primary.max_value = val
            self.state.save_snapshot()
            self.on_change()
        except ValueError:
            pass
    
    def _on_y2_label_change(self, e):
        """Handle secondary Y label change."""
        if self.state.chart_config.y_axis_secondary:
            self.state.chart_config.y_axis_secondary.label = e.control.value
            self.state.save_snapshot()
            self.on_change()
    
    def _on_y2_scale_change(self, e):
        """Handle secondary Y scale change."""
        if self.state.chart_config.y_axis_secondary:
            self.state.chart_config.y_axis_secondary.scale = e.control.value
            self.state.save_snapshot()
            self.on_change()
    
    def _build_layout_section(self) -> ft.Control:
        """Build layout configuration."""
        content = ft.Column([
            LabeledControl(
                "Title",
                ft.TextField(
                    value=self.state.chart_config.title,
                    on_change=self._on_title_change,
                    height=50,
                    text_size=13,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
            LabeledControl(
                "Subtitle",
                ft.TextField(
                    value=self.state.chart_config.subtitle,
                    on_change=self._on_subtitle_change,
                    height=50,
                    text_size=13,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=10),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
            LabeledControl(
                "Legend",
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("best", "Best"),
                        ft.dropdown.Option("upper right", "Upper Right"),
                        ft.dropdown.Option("upper left", "Upper Left"),
                        ft.dropdown.Option("lower left", "Lower Left"),
                        ft.dropdown.Option("lower right", "Lower Right"),
                        ft.dropdown.Option("none", "None"),
                    ],
                    value=self.state.chart_config.legend_position,
                    on_change=self._on_legend_change,
                    height=55,
                    text_size=12,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
        ], spacing=10)
        
        return Section("Layout & Labels", content, expanded=self.section_expanded.get(5, True))
    
    def _on_title_change(self, e):
        """Handle title change."""
        self.state.chart_config.title = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_subtitle_change(self, e):
        """Handle subtitle change."""
        self.state.chart_config.subtitle = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_legend_change(self, e):
        """Handle legend position change."""
        self.state.chart_config.legend_position = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _build_annotations_section(self) -> ft.Control:
        """Build annotations section."""
        annotation_type_selector = ft.Dropdown(
            options=[
                ft.dropdown.Option("hline", "Horizontal Line"),
                ft.dropdown.Option("vline", "Vertical Line"),
                ft.dropdown.Option("text", "Text Label"),
                ft.dropdown.Option("span", "Horizontal Span"),
                ft.dropdown.Option("band", "Vertical Band"),
            ],
            value="hline",
            width=180,
            height=55,
            text_size=12,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
            bgcolor=ft.colors.SURFACE_VARIANT,
            color=ft.colors.ON_SURFACE,
            border_color=ft.colors.OUTLINE,
        )
        
        add_btn = ft.ElevatedButton(
            "Add",
            icon=ft.icons.ADD,
            on_click=lambda e: self._on_add_annotation(e, annotation_type_selector.value),
            height=35,
        )
        
        annotations_list = ft.Column(
            [self._build_annotation_control(ann, i) 
             for i, ann in enumerate(self.state.chart_config.annotations)],
            spacing=5,
        )
        
        content = ft.Column([
            ft.Row([annotation_type_selector, add_btn], spacing=5),
            annotations_list,
        ], spacing=10)
        
        return Section("Annotations", content, expanded=self.section_expanded.get(6, False))
    
    def _build_annotation_control(self, annotation: Annotation, index: int) -> ft.Control:
        """Build control for single annotation."""
        # Build parameter controls based on annotation type
        param_controls = []
        
        if annotation.annotation_type == "hline":
            param_controls = [
                LabeledControl(
                    "Y Value",
                    ft.TextField(
                        value=str(annotation.params.get("y", 0)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "y", float(e.control.value) if e.control.value else 0),
                        height=45,
                        text_size=12,
                        width=100,
                    ),
                ),
                LabeledControl(
                    "Color",
                    ft.TextField(
                        value=annotation.params.get("color", "red"),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "color", e.control.value),
                        height=45,
                        text_size=12,
                        width=100,
                    ),
                ),
            ]
        elif annotation.annotation_type == "vline":
            param_controls = [
                LabeledControl(
                    "X Value",
                    ft.TextField(
                        value=str(annotation.params.get("x", 0)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "x", float(e.control.value) if e.control.value else 0),
                        height=45,
                        text_size=12,
                        width=100,
                    ),
                ),
                LabeledControl(
                    "Color",
                    ft.TextField(
                        value=annotation.params.get("color", "red"),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "color", e.control.value),
                        height=45,
                        text_size=12,
                        width=100,
                    ),
                ),
            ]
        elif annotation.annotation_type == "text":
            param_controls = [
                LabeledControl(
                    "Text",
                    ft.TextField(
                        value=annotation.params.get("text", ""),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "text", e.control.value),
                        height=45,
                        text_size=12,
                    ),
                ),
                LabeledControl(
                    "X",
                    ft.TextField(
                        value=str(annotation.params.get("x", 0)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "x", float(e.control.value) if e.control.value else 0),
                        height=45,
                        text_size=12,
                        width=80,
                    ),
                ),
                LabeledControl(
                    "Y",
                    ft.TextField(
                        value=str(annotation.params.get("y", 0)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "y", float(e.control.value) if e.control.value else 0),
                        height=45,
                        text_size=12,
                        width=80,
                    ),
                ),
            ]
        elif annotation.annotation_type == "span":
            param_controls = [
                LabeledControl(
                    "X Min",
                    ft.TextField(
                        value=str(annotation.params.get("xmin", 0)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "xmin", float(e.control.value) if e.control.value else 0),
                        height=45,
                        text_size=12,
                        width=80,
                    ),
                ),
                LabeledControl(
                    "X Max",
                    ft.TextField(
                        value=str(annotation.params.get("xmax", 1)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "xmax", float(e.control.value) if e.control.value else 1),
                        height=45,
                        text_size=12,
                        width=80,
                    ),
                ),
                LabeledControl(
                    "Color",
                    ft.TextField(
                        value=annotation.params.get("color", "yellow"),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "color", e.control.value),
                        height=45,
                        text_size=12,
                        width=100,
                    ),
                ),
            ]
        elif annotation.annotation_type == "band":
            param_controls = [
                LabeledControl(
                    "Y Min",
                    ft.TextField(
                        value=str(annotation.params.get("ymin", 0)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "ymin", float(e.control.value) if e.control.value else 0),
                        height=45,
                        text_size=12,
                        width=80,
                    ),
                ),
                LabeledControl(
                    "Y Max",
                    ft.TextField(
                        value=str(annotation.params.get("ymax", 1)),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "ymax", float(e.control.value) if e.control.value else 1),
                        height=45,
                        text_size=12,
                        width=80,
                    ),
                ),
                LabeledControl(
                    "Color",
                    ft.TextField(
                        value=annotation.params.get("color", "gray"),
                        on_change=lambda e, idx=index: self._on_annotation_param_change(idx, "color", e.control.value),
                        height=45,
                        text_size=12,
                        width=100,
                    ),
                ),
            ]
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Checkbox(
                        value=annotation.enabled,
                        on_change=lambda e, idx=index: self._on_annotation_toggle(e, idx),
                    ),
                    ft.Text(annotation.annotation_type.upper(), size=12, weight=ft.FontWeight.W_500, expand=True),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        icon_size=16,
                        on_click=lambda _, idx=index: self._on_delete_annotation(idx),
                    ),
                ], alignment=ft.MainAxisAlignment.START),
                ft.Container(
                    content=ft.Column(param_controls, spacing=5),
                    padding=ft.padding.only(left=30),
                    visible=annotation.enabled,
                ) if param_controls else ft.Container(),
            ], spacing=5),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=4,
            padding=8,
        )
    
    def _on_add_annotation(self, e, annotation_type: str = "hline"):
        """Add new annotation."""
        # Create default params based on type
        default_params = {
            "hline": {"y": 0, "color": "red", "linestyle": "--"},
            "vline": {"x": 0, "color": "red", "linestyle": "--"},
            "text": {"x": 0, "y": 0, "text": "Label", "fontsize": 10},
            "span": {"xmin": 0, "xmax": 1, "color": "yellow"},
            "band": {"ymin": 0, "ymax": 1, "color": "gray"},
        }
        
        params = default_params.get(annotation_type, {"color": "red"}        )
        self.state.chart_config.annotations.append(
            Annotation(annotation_type=annotation_type, params=params)
        )
        self.state.save_snapshot()
        # Rebuild the annotations section only
        self._rebuild_section(6)  # Annotations section is at index 6
        self.on_change()
    
    def _on_annotation_toggle(self, e, index: int):
        """Toggle annotation."""
        self.state.chart_config.annotations[index].enabled = e.control.value
        self.state.save_snapshot()
        # Rebuild to show/hide parameter controls
        self._rebuild_section(6)
        self.on_change()
    
    def _on_annotation_param_change(self, index: int, param_name: str, value):
        """Handle annotation parameter change."""
        try:
            self.state.chart_config.annotations[index].params[param_name] = value
            self.state.save_snapshot()
            self.on_change()
        except (IndexError, KeyError):
            pass
    
    def _on_delete_annotation(self, index: int):
        """Delete annotation."""
        self.state.chart_config.annotations.pop(index)
        self.state.save_snapshot()
        # Rebuild the annotations section only
        self._rebuild_section(6)  # Annotations section is at index 6
        self.on_change()
    
    def _build_theme_section(self) -> ft.Control:
        """Build theme configuration."""
        content = ft.Column([
            LabeledControl(
                "Mode",
                ft.Dropdown(
                    options=[
                        ft.dropdown.Option("light", "Light"),
                        ft.dropdown.Option("dark", "Dark"),
                    ],
                    value=self.state.theme.mode,
                    on_change=self._on_theme_mode_change,
                    height=55,
                    text_size=12,
                    content_padding=ft.padding.symmetric(horizontal=10, vertical=8),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    color=ft.colors.ON_SURFACE,
                    border_color=ft.colors.OUTLINE,
                ),
            ),
            LabeledControl(
                "Font Size",
                ft.Slider(
                    min=8,
                    max=16,
                    value=self.state.theme.font_size,
                    on_change=self._on_font_size_change,
                    divisions=8,
                ),
            ),
        ], spacing=10)
        
        return Section("Theme & Styling", content, expanded=self.section_expanded.get(7, False))
    
    def _on_theme_mode_change(self, e):
        """Handle theme mode change."""
        self.state.theme.mode = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_font_size_change(self, e):
        """Handle font size change."""
        self.state.theme.font_size = e.control.value
        self.state.save_snapshot()
        self.on_change()
    
    def _on_cell_edit(self, e, row_idx: int, col_idx: int):
        """Handle cell value edit."""
        if self.state.data_source is None:
            return
        
        try:
            new_value = e.control.value
            col_name = self.state.data_source.df.columns[col_idx]
            
            # Try to infer and convert the type
            if new_value == "":
                self.state.data_source.df.iloc[row_idx, col_idx] = None
            else:
                # Try numeric conversion
                try:
                    if '.' in new_value:
                        converted_value = float(new_value)
                    else:
                        converted_value = int(new_value)
                    self.state.data_source.df.iloc[row_idx, col_idx] = converted_value
                except ValueError:
                    # Keep as string
                    self.state.data_source.df.iloc[row_idx, col_idx] = new_value
            
            self.state.save_snapshot()
            self.on_change()
        except Exception as ex:
            print(f"Error editing cell: {ex}")
    
    def _on_add_row(self, e):
        """Add a new row to the data."""
        if self.state.data_source is None:
            return
        
        import pandas as pd
        import numpy as np
        
        # Create a new row with default values (0 for numeric, empty string for others)
        new_row = {}
        for col in self.state.data_source.df.columns:
            dtype = self.state.data_source.df[col].dtype
            if pd.api.types.is_numeric_dtype(dtype):
                new_row[col] = 0
            else:
                new_row[col] = ""
        
        # Append the new row
        self.state.data_source.df = pd.concat(
            [self.state.data_source.df, pd.DataFrame([new_row])],
            ignore_index=True
        )
        
        self.state.save_snapshot()
        # Rebuild data editor to show new row
        self._rebuild_section(1)
        self.on_change()
    
    def _on_delete_row(self, e):
        """Delete the last row from the data."""
        if self.state.data_source is None or len(self.state.data_source.df) == 0:
            return
        
        # Remove last row
        self.state.data_source.df = self.state.data_source.df.iloc[:-1]
        
        self.state.save_snapshot()
        # Rebuild data editor to reflect deletion
        self._rebuild_section(1)
        self.on_change()
    
    def _on_add_column(self, e):
        """Add a new column to the data."""
        if self.state.data_source is None:
            return
        
        # Find a unique column name
        base_name = "NewColumn"
        col_name = base_name
        counter = 1
        while col_name in self.state.data_source.df.columns:
            col_name = f"{base_name}{counter}"
            counter += 1
        
        # Add the column with default value 0
        self.state.data_source.df[col_name] = 0
        
        self.state.save_snapshot()
        # Rebuild data editor and series section to show new column
        self._rebuild_section(1)
        self._rebuild_section(3)
        self.on_change()
    
    def _on_delete_column(self, col_idx: int):
        """Delete a column from the data."""
        if self.state.data_source is None or col_idx >= len(self.state.data_source.df.columns):
            return
        
        col_name = self.state.data_source.df.columns[col_idx]
        
        # Don't delete if it's the last column
        if len(self.state.data_source.df.columns) <= 1:
            return
        
        # Remove column
        self.state.data_source.df = self.state.data_source.df.drop(columns=[col_name])
        
        # Remove any series that used this column
        self.state.chart_config.series_styles = [
            s for s in self.state.chart_config.series_styles 
            if s.column != col_name
        ]
        
        # Update X column if it was deleted
        if self.state.chart_config.x_column == col_name:
            self.state.chart_config.x_column = self.state.data_source.df.columns[0] if len(self.state.data_source.df.columns) > 0 else None
        
        self.state.save_snapshot()
        # Rebuild data editor and series section
        self._rebuild_section(1)
        self._rebuild_section(3)
        self.on_change()
    
    def _on_column_rename(self, e, col_idx: int):
        """Rename a column."""
        if self.state.data_source is None or col_idx >= len(self.state.data_source.df.columns):
            return
        
        old_name = self.state.data_source.df.columns[col_idx]
        new_name = e.control.value.strip()
        
        # Don't rename if empty or same
        if not new_name or new_name == old_name:
            return
        
        # Don't rename if name already exists
        if new_name in self.state.data_source.df.columns:
            e.control.value = old_name
            return
        
        # Rename the column
        self.state.data_source.df = self.state.data_source.df.rename(columns={old_name: new_name})
        
        # Update series that used this column
        for series in self.state.chart_config.series_styles:
            if series.column == old_name:
                series.column = new_name
        
        # Update X column if it was renamed
        if self.state.chart_config.x_column == old_name:
            self.state.chart_config.x_column = new_name
        
        self.state.save_snapshot()
        # Rebuild series section to show updated column names
        self._rebuild_section(3)
        self.on_change()
    
    def _on_export_data_csv(self, e):
        """Export current data as CSV."""
        if self.state.data_source is None:
            return
        
        # Trigger the main export flow
        self.on_import_data("export_csv")
    
    def _rebuild_section(self, section_index: int):
        """Rebuild a specific section without affecting scroll position.
        
        Section indices:
        0 = Data Sources
        1 = Data Editor
        2 = Chart Type
        3 = Series
        4 = Axes & Scales
        5 = Layout & Labels
        6 = Annotations
        7 = Theme & Styling
        """
        # Preserve the current expansion state before rebuilding
        if section_index < len(self.sections_column.controls):
            current_section = self.sections_column.controls[section_index]
            if hasattr(current_section, 'is_expanded'):
                self.section_expanded[section_index] = current_section.is_expanded
        
        section_builders = [
            self._build_data_section,
            self._build_data_preview_section,
            self._build_chart_type_section,
            self._build_series_section,
            self._build_axes_section,
            self._build_layout_section,
            self._build_annotations_section,
            self._build_theme_section,
        ]
        
        if 0 <= section_index < len(section_builders):
            # Rebuild the specific section
            self.sections_column.controls[section_index] = section_builders[section_index]()
            # Update only the sections column
            self.sections_column.update()
    
    def refresh(self):
        """Refresh builder UI with current state."""
        # Preserve expansion states before refresh
        for i, section in enumerate(self.sections_column.controls):
            if hasattr(section, 'is_expanded'):
                self.section_expanded[i] = section.is_expanded
        
        # Rebuild all sections with current state
        self.sections_column.controls = [
            self._build_data_section(),
            self._build_data_preview_section(),
            self._build_chart_type_section(),
            self._build_series_section(),
            self._build_axes_section(),
            self._build_layout_section(),
            self._build_annotations_section(),
            self._build_theme_section(),
        ]
        
        if hasattr(self.sections_column, 'update'):
            self.sections_column.update()


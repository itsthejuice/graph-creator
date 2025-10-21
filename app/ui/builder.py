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
        
        # Build UI
        content = ft.Column([
            self._build_header(),
            ft.Divider(),
            ft.Container(
                content=ft.Column([
                    self._build_data_section(),
                    self._build_chart_type_section(),
                    self._build_series_section(),
                    self._build_axes_section(),
                    self._build_layout_section(),
                    self._build_annotations_section(),
                    self._build_theme_section(),
                ], spacing=10, scroll=ft.ScrollMode.AUTO),
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
            ft.Row([
                examples_menu,
                import_menu,
            ], alignment=ft.MainAxisAlignment.START),
            data_info,
        ], spacing=5)
        
        return Section("Data Sources", content)
    
    def _get_data_info(self) -> str:
        """Get data source info text."""
        if self.state.data_source is None:
            return "No data loaded. Load an example or import data."
        
        df = self.state.get_transformed_data()
        if df is None:
            return "No data available."
        
        return f"{len(df)} rows × {len(df.columns)} columns"
    
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
            height=50,
        )
        
        content = ft.Column([
            LabeledControl("Type", chart_type),
        ])
        
        return Section("Chart Type", content)
    
    def _on_chart_type_change(self, e):
        """Handle chart type change."""
        self.state.chart_config.chart_type = e.control.value
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
            height=50,
        )
        
        # Auto-create series styles if needed
        if not self.state.chart_config.series_styles:
            self._auto_create_series()
        
        # Series list
        series_controls = []
        for i, series in enumerate(self.state.chart_config.series_styles):
            series_controls.append(
                self._build_series_control(series, i)
            )
        
        content = ft.Column([
            x_column,
            ft.Divider(),
            *series_controls,
        ], spacing=10)
        
        return Section("Series", content, expanded=True)
    
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
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Checkbox(
                        value=series.visible,
                        on_change=lambda e, idx=index: self._on_series_visible_change(e, idx),
                    ),
                    ft.Text(series.column, size=12, weight=ft.FontWeight.W_500),
                ]),
                ft.Container(
                    content=ft.Column([
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
                            "Style",
                            ft.Dropdown(
                                options=[
                                    ft.dropdown.Option("solid", "Solid"),
                                    ft.dropdown.Option("dashed", "Dashed"),
                                    ft.dropdown.Option("dotted", "Dotted"),
                                    ft.dropdown.Option("dashdot", "Dash-Dot"),
                                ],
                                value=series.line_style,
                                on_change=lambda e, idx=index: self._on_series_style_change(e, idx),
                                height=45,
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
                                height=45,
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
        self.on_change()
    
    def _on_series_visible_change(self, e, index: int):
        """Handle series visibility change."""
        self.state.chart_config.series_styles[index].visible = e.control.value
        self.on_change()
    
    def _on_series_width_change(self, e, index: int):
        """Handle series line width change."""
        self.state.chart_config.series_styles[index].line_width = e.control.value
        self.on_change()
    
    def _on_series_style_change(self, e, index: int):
        """Handle series line style change."""
        self.state.chart_config.series_styles[index].line_style = e.control.value
        self.on_change()
    
    def _on_series_axis_change(self, e, index: int):
        """Handle series axis change."""
        self.state.chart_config.series_styles[index].y_axis = e.control.value
        self.on_change()
    
    def _build_axes_section(self) -> ft.Control:
        """Build axes configuration."""
        content = ft.Column([
            ft.Text("Primary Y Axis", size=12, weight=ft.FontWeight.BOLD),
            LabeledControl(
                "Label",
                ft.TextField(
                    value=self.state.chart_config.y_axis_primary.label,
                    on_change=self._on_y_label_change,
                    height=40,
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
                    height=45,
                ),
            ),
            LabeledControl(
                "Grid",
                ft.Switch(
                    value=self.state.chart_config.y_axis_primary.show_grid,
                    on_change=self._on_grid_change,
                ),
            ),
        ], spacing=10)
        
        return Section("Axes & Scales", content)
    
    def _on_y_label_change(self, e):
        """Handle Y label change."""
        self.state.chart_config.y_axis_primary.label = e.control.value
        self.on_change()
    
    def _on_y_scale_change(self, e):
        """Handle Y scale change."""
        self.state.chart_config.y_axis_primary.scale = e.control.value
        self.on_change()
    
    def _on_grid_change(self, e):
        """Handle grid toggle."""
        self.state.chart_config.y_axis_primary.show_grid = e.control.value
        self.on_change()
    
    def _build_layout_section(self) -> ft.Control:
        """Build layout configuration."""
        content = ft.Column([
            LabeledControl(
                "Title",
                ft.TextField(
                    value=self.state.chart_config.title,
                    on_change=self._on_title_change,
                    height=40,
                ),
            ),
            LabeledControl(
                "Subtitle",
                ft.TextField(
                    value=self.state.chart_config.subtitle,
                    on_change=self._on_subtitle_change,
                    height=40,
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
                    height=45,
                ),
            ),
        ], spacing=10)
        
        return Section("Layout & Labels", content)
    
    def _on_title_change(self, e):
        """Handle title change."""
        self.state.chart_config.title = e.control.value
        self.on_change()
    
    def _on_subtitle_change(self, e):
        """Handle subtitle change."""
        self.state.chart_config.subtitle = e.control.value
        self.on_change()
    
    def _on_legend_change(self, e):
        """Handle legend position change."""
        self.state.chart_config.legend_position = e.control.value
        self.on_change()
    
    def _build_annotations_section(self) -> ft.Control:
        """Build annotations section."""
        add_btn = ft.ElevatedButton(
            "Add Annotation",
            icon=ft.icons.ADD,
            on_click=self._on_add_annotation,
        )
        
        annotations_list = ft.Column(
            [self._build_annotation_control(ann, i) 
             for i, ann in enumerate(self.state.chart_config.annotations)],
            spacing=5,
        )
        
        content = ft.Column([
            add_btn,
            annotations_list,
        ], spacing=10)
        
        return Section("Annotations", content, expanded=False)
    
    def _build_annotation_control(self, annotation: Annotation, index: int) -> ft.Control:
        """Build control for single annotation."""
        return ft.Container(
            content=ft.Row([
                ft.Checkbox(
                    value=annotation.enabled,
                    on_change=lambda e, idx=index: self._on_annotation_toggle(e, idx),
                ),
                ft.Text(annotation.annotation_type, size=12),
                ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_size=16,
                    on_click=lambda _, idx=index: self._on_delete_annotation(idx),
                ),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=4,
            padding=5,
        )
    
    def _on_add_annotation(self, e):
        """Add new annotation."""
        # Add a simple horizontal line as default
        self.state.chart_config.annotations.append(
            Annotation(annotation_type="hline", params={"y": 0, "color": "red"})
        )
        self.on_change()
    
    def _on_annotation_toggle(self, e, index: int):
        """Toggle annotation."""
        self.state.chart_config.annotations[index].enabled = e.control.value
        self.on_change()
    
    def _on_delete_annotation(self, index: int):
        """Delete annotation."""
        self.state.chart_config.annotations.pop(index)
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
                    height=45,
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
        
        return Section("Theme & Styling", content, expanded=False)
    
    def _on_theme_mode_change(self, e):
        """Handle theme mode change."""
        self.state.theme.mode = e.control.value
        self.on_change()
    
    def _on_font_size_change(self, e):
        """Handle font size change."""
        self.state.theme.font_size = e.control.value
        self.on_change()
    
    def refresh(self):
        """Refresh builder UI with current state."""
        # This would rebuild the UI - for now just update
        if hasattr(self, 'update'):
            self.update()

